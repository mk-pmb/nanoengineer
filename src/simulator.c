// Copyright (c) 2004 Nanorex, Inc. All Rights Reserved.
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <signal.h>

#include "simulator.h"

int debug_flags = 0;

int interrupted = 0; /* set to 1 when a SIGTERM is received */

/** indicate next avail/total number of stretch bonds, bend bonds, and atoms */
int Nexbon=0, Nextorq=0, Nexatom=0;

/* factor for a unit vector given length squared -- rtned in uf, i is temp */
/** tables and setup function for same */
double uft1[UFTLEN], uft2[UFTLEN];

double uffunc(double uf) {
    return 1.0/sqrt(uf);
}

/** positions and forces on the atoms */
// units for positions are 1e-12 meters == picometers
// units for force are piconewtons
struct xyz force[NATOMS];
struct xyz old_force[NATOMS]; /* used in minimize */
struct xyz average_positions[NATOMS];
struct xyz position_arrays[3*NATOMS];
struct xyz *old_positions, *new_positions, *positions; // these point into position_arrays


struct xyz Center, Bbox[2];

/** data for the 5-carbon test molecule */
struct xyz diam[5]=
    {{0.0, 0.0, 0.0},
     {176.7, 176.7, 0.0},
     {176.7, 0.0, 176.7},
     {0.0, 176.7, 176.7},
     {88.33, 88.33, 88.33}};

int PartNo=0, DisplayStyle=1;	/* 0 nothing, 1 ball/stick, 2 vdW surface */

struct A atom[NATOMS];

struct B bond[4*NATOMS];

struct Q torq[6*NATOMS];


int Iteration=0;


int findbond(int btyp) {
    int i;
    if (btyp < 0)
	btyp = -btyp;
    for (i=0; i < BSTABSIZE; i++)
	if (bstab[i].typ == btyp)
	    return i;
    // fprintf(stderr, "Bond type %d not found\n",btyp);
    return -1;
}

int findtorq(int btyp1, int btyp2) {
    int i;
    for (i=0; i < BENDATASIZE; i++) {
		
	if  (iabs(bendata[i].b1typ) == iabs(btyp1) &&
	     iabs(bendata[i].b2typ) == iabs(btyp2)) return i;
	if  (iabs(bendata[i].b1typ) == iabs(btyp2) &&
	     iabs(bendata[i].b2typ) == iabs(btyp1)) return i;
    }
    // fprintf(stderr, "Bend type %d-%d not found\n",btyp1,btyp2);
    return 0; // the default bend type
}

/** the force between elt i and elt j (i<=j) is at
    vanderTable[i*(NUMELTS+1) - i*(i+1)/2 + j-i] */
// struct vdWtab vanderTable[(NUMELTS * (NUMELTS+1))/2];
struct vdWtab vanderTable[(50 * 51)/2];

double RvdW, EvdW;

struct vdWbuf *Nexvanbuf, *Dynobuf;
int Dynoix;			/* start of dynamically found vdw's */

/** A space grid for locating non-bonded interactions */

struct A *Space[SPWIDTH][SPWIDTH][SPWIDTH];	/*  space buckets */

void orion() {			/* atoms in space :-) */
    int n, i,j,k;
    struct A **pail;

    for (n=0; n<Nexatom; n++) *atom[n].bucket = NULL;
	
    for (n=0; n<Nexatom; n++) {
	i= ((int)positions[n].x / 250) & SPMASK;
	j= ((int)positions[n].y / 250) & SPMASK;
	k= ((int)positions[n].z / 250) & SPMASK;

	pail = &Space[i][j][k];
	atom[n].next = *pail;
	*pail = atom+n;
	atom[n].bucket = pail;
    }

}


/** constraints */

int Nexcon=0;

struct AXLE Constraint[100];


/** motors: shoot for 5 nN/atom? speeds up to 10 m/s */

int Nexmot=0;

struct MOT Motor[100];




/** constants: timestep (.1 femtosecond), scale of distance (picometers) */
double Dt= 1e-16, Dx=1e-12;
double Dmass = 1e-27;           // units of mass vs. kg
double Temperature = 300.0;	/* Kelvins */
double Boltz = 1.38e-23;	/* k, in J/K */

double TotalKE = 0.0;		 /* actually double, = m_i v_i^2 */
double FoundKE = 0.0;

double Pi = 3.1415926;

/* values are for carbon and carbon-carbon bond (for testing) */

/** stiffnesses are in N/m, so forces come out in pN (i.e. Dx N) */
double Kb=28.63;		/* N/m */
double Ks=440.0;		/* N/m */
double De=0.556, Beta = 1.989e-2; /* Morse params */

//NB depends on Dx
double Tq = 1e-3;            // since torques are given in pN*nm,
     // force(pN) = Tq(Dx/nm)*torque(pN*nm)/r(Dx)

/** pN/kg => acc in pm/s^2; mult by Dt^2 (folded into massacc) */

double R0 = 152.3, R1 = 152.3, Theta0 = 1.911;

/** global properties: center of mass, momentum, moment of rotation */
double totMass=0.0;
struct xyz Cog, P, Omega;

double totClipped=0.0;  // internal thermostat for numerical stability

double Gamma = 0.01; // for Langevin thermostats
// double G1=(1.01-0.27*Gamma)*1.4*sqrt(Gamma);
double G1=(1.01-0.27*0.01)*1.4*0.1;

// definitions for command line args

int ToMinimize=0;
int IterPerFrame=10;
int NumFrames=100;
int DumpAsText=0;
int PrintFrameNums=1;

char OutFileName[1024];
char TraceFileName[1024];

// for writing the differential position and trace files
FILE *outf, *tracef;
int *ixyz, *previxyz, *temp, ibuf1[NATOMS*3], ibuf2[NATOMS*3];


/* for testing table routines */
double t1[TABLEN], t2[TABLEN];
double start=10000.0;
int scale=30;

/* Make a table for interpolating func(x) by doing
   i=(int)(x-start)/scale;
   value=t1[i]+x*t2[i]; */

void maktab(double *t1, double *t2, double func(double),
	    double start, int length, int scale) {
    int i;
    double v1, v2, r1, r2, q;
    double ov1, v3, r5, r15, v5, v15;
	
    r2=start;
    v2=func(r2);
	
    for (i=0; i<length; i++) {
	r1=r2;
	v1=v2;
	r2=start+(double)((i+1)*scale);
	v2=func(r2);
	/* shift points to minimize excursions above/below func */
	if (i<length-1) {
	    r5=(r1+r2)/2.0;
	    r15=r2+r2-r5;
	    v5=func(r5);
	    v15=func(r15);
	    v3=func(r2+r2-r1);
	    v2=v2 + 0.25*(v5-(func(r1)+v2)/2.0) + 0.25*(v15-(v2+v3)/2.0);
	}
		
	q=(v2-v1)/(r2-r1);
	t1[i] = v1 - q*r1;
	t2[i] = q;
    }
}

/* consider atoms a0 and a1 both bonded to atom ac.
   We are given the length of (a0-ac)+(a1-ac), squared, and
   desire to calculate a factor which multiplied by (a1-ac)
   gives the appropriate bending force for a0 */

/* uses globals R0 and R1, the lengths of (a0-ac) & (a1-ac), in pm,
   Kb, in N/m, and Theta0, the nominal angle, in radians */

double bender(double rSquared) {
    double theta,f;
    theta=acos((rSquared-(R0*R0+R1*R1))/(2.0*R0*R1));
	
    if (theta < Theta0)
	f= - Kb*(exp(-2.0*(theta-Theta0)) - exp(-(theta-Theta0)));
    else f=  Kb*sin(Pi * (theta - Theta0) / (Pi - Theta0))*(Pi - Theta0)/Pi;
	
	
    return R0*f / (R1 * sin(theta));
}

/** note -- uses global Ks and R0 */
// a kludge, no coherent units; result will be interpreted as pN
double hooke(double rSquared) {
	double r;
	
	r=sqrt(rSquared);
	return 2.0*Ks*(R0/r-1.0);
	//return Ks*(R0-r);
}

/* use the Morse potential inside R0, Lippincott outside */
/* numerically differentiate the resulting potential for force */
/* uses global De, Beta, Ks and R0 */

// the result is in attoJoules per picometer * 1e6 = picoNewtons
double lippmor(double rSquared) {
    double r,y1,y2;
	
    r=sqrt(rSquared);
    r=r+0.5;
	
    if (r>=R0)
	y2=De *(1-exp(- 1e-6 * Ks * R0 * (r - R0)* (r - R0) / (2 *De* r)));
    else
	y2=De *(1-exp(- Beta * (r - R0))) *(1-exp(- Beta * (r - R0)));
	
    r=r-1.0;
	
    if (r>=R0)
	y1=De *(1-exp(- 1e-6 * Ks * R0 * (r - R0)* (r - R0) / (2 *De* r)));
    else
	y1=De *(1-exp(- Beta * (r - R0))) *(1-exp(- Beta * (r - R0)));
	
    r=r+0.5;
	
    return 1e6*(y1-y2)/r;
}

/* the Buckingham potential for van der Waals / London force */
/* uses global EvdW, RvdW */
double bucking(double rSquared) {
    double r, y;
    r=sqrt(rSquared);
	
    y= -1e3 * EvdW*(2.48e5 * exp(-12.5*(r/RvdW)) *(-12.5/RvdW)
		    -1.924*pow(1.0/RvdW, -6.0)*(-6.0)*pow(r,-7.0));
	
    return y/r;
}

double square(double x) {return x*x;}

/* initialize the function tables for each bending and stretching bondtype */
/* sets global De, Beta, Ks and R0 */
void bondinit() {
    int i, j, b1,b2;
    double end, m, rxsq;
    struct dtab *tables,*t2;
	
    for (i=0; i < BSTABSIZE; i++) {
		
	R0 = bstab[i].r0;
	bstab[i].start = square(R0*0.5);
	end = square(R0*1.5);
	bstab[i].scale = (end - bstab[i].start) / TABLEN;
	Ks = bstab[i].ks;
	De = bstab[i].de;
	Beta = bstab[i].beta;
	tables = malloc(sizeof(struct dtab));
	//	if (ToMinimize)
	//    	maktab(tables->t1, tables->t2, hooke,
	//	       bstab[i].start, TABLEN, bstab[i].scale);
	//else 
	maktab(tables->t1, tables->t2, lippmor,
		    bstab[i].start, TABLEN, bstab[i].scale);
	bstab[i].table = tables;
    }
	
}

void vdWsetup() {
    int i, j, k, nx, scale;
    double x, y, start, end;
	
    for (i=0; i<NUMELTS; i++)
	for (j=0; j<NUMELTS; j++)
	    if (i<=j) {
		RvdW = 100.0 * (element[i].rvdw + element[j].rvdw);
		EvdW = (element[i].evdw + element[j].evdw)/2.0;
				
		nx = i*(NUMELTS+1) - i*(i+1)/2 + j-i;
				
		start= square(RvdW*0.4);
		end=square(RvdW*1.5);
		scale = (int)(end - start) / TABLEN;
				
		vanderTable[nx].start = start;
		vanderTable[nx].scale = scale;
				
		maktab(vanderTable[nx].table.t1, vanderTable[nx].table.t2,
		       bucking, start, TABLEN, scale);
				
	    }
	
    Nexvanbuf = &vanderRoot;
    Nexvanbuf->fill = 0;
    Nexvanbuf->next = NULL;
	
    /* the space grid */
    for (i=0;i<SPWIDTH; i++)
	for (j=0;j<SPWIDTH; j++)
	    for (k=0;k<SPWIDTH; k++)
		Space[i][j][k] = NULL;
	
}

/** kT @ 300K is 4.14 zJ -- RMS V of carbon is 1117 m/s
    or 645 m/s each dimension, or 0.645 pm/fs  */

double gavss(double v) {
    double v0,v1, rSquared;
    do {
	v0=(float)rand()/(float)(RAND_MAX/2) - 1.0;
	v1=(float)rand()/(float)(RAND_MAX/2) - 1.0;
	rSquared = v0*v0 + v1*v1;
    } while (rSquared>=1.0 || rSquared==0.0);
    return v*v0*sqrt(-2.0*log(rSquared)/rSquared);
}

struct xyz gxyz(double v) {
    struct xyz g;
    g.x=gavss(v);
    g.y=gavss(v);
    g.z=gavss(v);
    return g;
}

struct xyz sxyz(double *v) {
    struct xyz g;
    g.x=v[0];
    g.y=v[1];
    g.z=v[2];
    return g;
}

int isbonded(int a1, int a2) {
    int j, b, ba;
	for (j=0; j<atom[a1].nbonds; j++) {
	    b=atom[a1].bonds[j];
	    ba=(a1==bond[b].an1 ? bond[b].an2 : bond[b].an1);
	    if (ba==a2) return 1;
	}
	return 0;
}
    

int Count = 0;

void findnobo(int a1) {
    int a2, ix, iy, iz, i, j, k;
    struct A *p;
    double r;

    // fprintf(stderr, "find nobo for %d\n",a1);
	
    ix= (int)positions[a1].x / 250 + 4;
    iy= (int)positions[a1].y / 250 + 4;
    iz= (int)positions[a1].z / 250 + 4;

    for (i=ix-7; i<ix; i++)
	for (j=iy-7; j<iy; j++)
	    for (k=iz-7; k<iz; k++)
		for (p=Space[i&SPMASK][j&SPMASK][k&SPMASK]; p; p=p->next) {
		    a2 = p-atom;
		    if (a2>a1 
			// && (ToMinimize || atom[a1].part != atom[a2].part)
			&& !isbonded(a1,a2)) {
			r=vlen(vdif(positions[a1],positions[a2]));
			if (r<800.0) {
			    // fprintf(stderr, "  found nobo for %d<-->%d\n",a1, a2);
			    makvdw(a1, a2);
			    Count++;
			}
		    }
		}
}

// center of mass

struct xyz CoM(struct xyz *list) {
    int i,j, k;
    double x, y, z;
    struct xyz c, rx;

    vsetc(c,0.0);
    for (j=0; j<Nexatom; j++) {
	rx=vprodc(list[j],element[atom[j].elt].mass);
	vadd(c,rx);
    }
    vmulc(c,Dmass/totMass);
    return c;
}


// total kinetic energy over k
double totKE() {
    int i,j, k;
    double a,b,c;
    struct xyz f, v1, v2, rx;

    c=0.0;
    for (j=0; j<Nexatom; j++) {
        rx=vdif(positions[j], old_positions[j]);
        a=vdot(rx,rx)*Dx*Dx/(Dt*Dt);
        a *= element[atom[j].elt].mass * 1e-27/ Boltz;
        c += a;
    }
    return c;
}

static int ShotNo=0;
static int innerIters = 100;

/*
  for minimization:
  
  inputs:
    old_positions[*]
    positions[*]
    bond[*].an1, .an2, .type
    torq[*].dir1, .dir2, .b1, .b2, .kb1, .kb2
    
  changes:
    finds non-bonded interacting atoms using orion()
    average_positions[*] = 0
    force[*] contains accumulated force on atom over calculated iterations
    bond[*].r = vector from bond[*].an1 to bond[*].an2 (delta of positions)
    bond[*].invlen = 1/|r|
    bond[*].ru = unit vector along r

  for dynamics (as above plus):

  inputs:
    Constraint[*].*

  changes:
    old_positions
    positions[*]
    new_positions[*]
    average_positions[*] = average position across all iterations for this call
    Constraint[*].*
*/
void calcloop(int iters) {
	
    double fac, ke;
    int i,j, k, loop, a1, a2, ac, n, orionp;
    double rSquared, ff, m, theta, z, sum_torque, motorq, omega;
    struct xyz f, v1, v2, rx, foo, bar, totforce, q1, q2;
    struct xyz *tmp;
    struct vdWbuf *nvb;
    struct MOT *mot;
	
    double *t1, *t2;
    double start, deltaTframe;
    int scale;

    double therm;

    orionp = iters;

    iters = max(iters,1);

    deltaTframe = 1.0/iters;
	
    for (j=0; j<Nexatom; j++) {
	vsetc(average_positions[j],0.0);
    }
	
    for (loop=0, i=innerIters; loop<iters && !interrupted; loop++, i--) {
		
	Iteration++;

	if (orionp && i==innerIters) {
	    /* find the non-bonded interactions */
	    orion();
		
	    Nexvanbuf=Dynobuf;
	    Nexvanbuf->fill = Dynoix;
	    Count = 0;
		
	    for (j=0; j<Nexatom; j++) {
		findnobo(j);
	    }
	    i=innerIters;
	}		
			
	/* new_positions, positions, and old_positions to avoid mixing positions while
	   calculating force
	   force calculated separately because used for other things */
			
	/* first, for each atom, find non-accelerated new pos and clear force */			
        /* Atom moved from old_positions to positions last time,
           now we move it the same amount from positions to new_positions */	
	for (j=0; j<Nexatom; j++) {
	    vsub2(f,positions[j],old_positions[j]);
	    /*
	      ff = vdot(f,f);
	      if (ff < atom[j].vlim)  ff=1.0;
	      else {
	      ke=(ff-atom[j].vlim)*Dx*Dx/(Dt*Dt);
	      ke *= element[atom[j].elt].mass * 1e-27/ Boltz;
	      totClipped += ke;
	      //fprintf(stderr, "clip %f \n", ke);
	      ff = atom[j].vlim/ff;
	      }
	      vmulc(f, ff);
	    */
	    vadd2(new_positions[j],positions[j],f);
				
	    vsetc(force[j],0.0);
	}
			
	/* compute stretch force for each bond, accumulating in force[atom] */
	for (j=0; j<Nexbon; j++) {
	    vsub2(bond[j].r, positions[bond[j].an1], positions[bond[j].an2]);
	    vset(f,bond[j].r);
	    rSquared = vdot(f,f);
				
	    /* while we're at it, set unit bond vector and clear bend force */
	    ff = 1.0/sqrt(rSquared); /* XXX if atoms are on top of each other, 1/0 !! */
	    bond[j].invlen = ff;
	    vmul2c(bond[j].ru,f,ff); /* unit vector along r */
	    //vsetc(bond[j].bff,0.0);
				
	    /* table setup for stretch, to be moved out of loop */
	    start=bond[j].type->start;
	    scale=bond[j].type->scale;
	    t1=bond[j].type->table->t1;
	    t2=bond[j].type->table->t2;
				
	    k=(int)(rSquared-start)/scale;
	    if (k<0) {
					
		if (!ToMinimize && DEBUG(D_TABLE_BOUNDS)) { //linear
		    fprintf(stderr, "stretch: low --");
		    pb(stderr, j);
		}
		fac=t1[0]+rSquared*t2[0];
	    }
	    else if (k>=TABLEN) {
					
		// fprintf(stderr, "stretch: high --");
		// pb(stderr, j);
		if (ToMinimize)  //flat
		    fac = t1[TABLEN-1]+((TABLEN-1)*scale+start)*t2[TABLEN-1];
		else fac=0.0;
	    }
	    else fac=t1[k]+rSquared*t2[k];
            // table lookup equivalent to: fac=lippmor(rSquared)
            
	    // vmul2c(bond[j].aff,f,fac);
	    vmul2c(f,f,fac);  // f = r * lippmor(rSquared)
	    vadd(force[bond[j].an1],f);
	    vsub(force[bond[j].an2],f);
	    //fprintf(stderr, "length %f, force %f \n", vlen(bond[j].r), sqrt(vdot(f,f)));
	    //fprintf(stderr, "inverse length %f \n", bond[j].invlen);
				
	}
			
	/* now the forces for each bend */
			
	for (j=0; j<Nextorq; j++) {

	    // v1, v2 are the vectors FROM the central atom TO the neighbors
	    if (torq[j].dir1) {vsetn(v1,torq[j].b1->ru);}
	    else {vset(v1,torq[j].b1->ru);}
	    if (torq[j].dir2) {vsetn(v2,torq[j].b2->ru);}
	    else {vset(v2,torq[j].b2->ru);}

	    z = vdot(v1,v2);
	    m = torq[j].kb1 * (torq[j].kb2 - z);
	    vmul2c(q1, v1, z);
	    vmul2c(q2, v2, z);
	    vsub(q1, v2);
	    vsub(q2, v1);
	    vmulc(q1, m * torq[j].b1->invlen);
	    vmulc(q2, m * torq[j].b2->invlen);
		    
	    /*
		
	    // v1, v2 are the vectors FROM the central atom TO the neighbors
	    if (torq[j].dir1) {vsetn(v1,torq[j].b1->r);}
	    else {vset(v1,torq[j].b1->r);}
	    if (torq[j].dir2) {vsetn(v2,torq[j].b2->r);}
	    else {vset(v2,torq[j].b2->r);}
				
	    // z = 1.0/sqrt(vdot(v1,v1)*vdot(v2,v2));
	    z = torq[j].b1->invlen * torq[j].b2->invlen;
	    theta = acos(vdot(v1, v2)*z);

	    v2x(foo, v1, v2);
	    foo=uvec(foo);
	    q1=uvec(vx(v1, foo));
	    q2=uvec(vx(foo, v2));
		
	    ff = (theta - torq[j].theta0) * torq[j].kb1 * torq[j].b1->invlen;
	    vmulc(q1,ff);
	    ff = (theta - torq[j].theta0) * torq[j].kb2 * torq[j].b2->invlen;
	    vmulc(q2,ff);
	    */

		
		
	    vadd(force[torq[j].ac],q1);
	    vsub(force[torq[j].a1],q1);
	    vadd(force[torq[j].ac],q2);
	    vsub(force[torq[j].a2],q2);
	    /*
	      fprintf(stderr, "dtheta %f, torq %f \n",theta - torq[j].theta0, 
	      sqrt(vdot(q1,q1)));
	    */
	}

	// fprintf(stderr, "about to do vdw loop\n");
	/* do the van der Waals/London forces */
	for (nvb=&vanderRoot; nvb; nvb=nvb->next)
	    for (j=0; j<nvb->fill; j++) {
		// fprintf(stderr, "in vdw loop\n");
		vsub2(f, positions[nvb->item[j].a1], positions[nvb->item[j].a2]);
		rSquared = vdot(f,f);
					
		if (rSquared>50.0*700.0*700.0 && DEBUG(D_TABLE_BOUNDS)) {
                    fprintf(stderr, "hi vdw: %f\n", sqrt(rSquared));
                    pvdw(stderr, nvb,j);
		    pa(stderr, nvb->item[j].a1);
		    pa(stderr, nvb->item[j].a2);
		}
					
		/*
		  fprintf(stderr, "Processing vdW %d/%d: atoms %d-%d, r=%f\n",
		  nvb-&vanderRoot, j,nvb->item[j].a1, nvb->item[j].a2,
		  sqrt(rSquared));
		*/
		/* table setup  */
		start=nvb->item[j].table->start;
		scale=nvb->item[j].table->scale;
		t1=nvb->item[j].table->table.t1;
		t2=nvb->item[j].table->table.t2;
					
		k=(int)(rSquared-start)/scale;
		if (k<0) {
		    if (!ToMinimize && DEBUG(D_TABLE_BOUNDS)) { //linear
			fprintf(stderr, "vdW: off table low -- r=%.2f \n",  sqrt(rSquared));
			pvdw(stderr, nvb,j);
		    }
		    k=0;
		    fac=t1[k]+rSquared*t2[k];
		}
		else if (k>=TABLEN) {
		    /*
		      fprintf(stderr, "vdW: off table high -- %d/%d: start=%.2f, scale=%d\n",
		      k,TABLEN, start, scale);
		    */
		    fac = 0.0;
		}
		else fac=t1[k]+rSquared*t2[k];
		vmulc(f,fac);
		vadd(force[nvb->item[j].a1],f);
		vsub(force[nvb->item[j].a2],f);
	    }
		
	if (ToMinimize) return;  // just calc forces, once

	// pre-force constraints
	for (j=0;j<Nexcon;j++) {	/* for each constraint */
	    if (Constraint[j].type == CODEmotor) { /* motor */
					
		mot=Constraint[j].motor;

		if (mot->speed==0.0) { // just add torque to force

		    // set the center of torque each time
		    n=Constraint[j].natoms;
		    vsetc(rx, 0.0);
		    for (k=0; k<n; k++) {
			vadd(rx,positions[Constraint[j].atoms[k]]);
		    }
		    vmulc(rx,1.0/(double)n);
		    mot->center = rx;

		    ff = Tq*mot->stall/n;
		    for (k=0; k<n; k++) {
			a1 = Constraint[j].atoms[k];
			rx = vdif(positions[a1],mot->center);
			f  = vprodc(vx(mot->axis,uvec(rx)),ff/vlen(rx));
			    
			//fprintf(stderr, "applying torque %f to %d: other force %f\n",
			//       vlen(f), a1, vlen(force[a1]));

			vadd(force[a1],f);
		    }
		    // data for printing speed trace
		    Constraint[j].temp = mot->stall; // torque

		    rx=uvec(vdif(positions[Constraint[j].atoms[0]],mot->center));
			
		    theta = atan2(vdot(rx,mot->rotz),vdot(rx,mot->roty));
		    /* update the motor's position */
		    if (theta>Pi) {
			mot->theta0 = mot->theta-2.0*Pi;
			mot->theta = theta-2.0*Pi;
		    }
		    else {
			mot->theta0 = mot->theta;
			mot->theta = theta;
		    }
		    theta = mot->theta - mot->theta0;

		    Constraint[j].data += theta * deltaTframe;
		}
	    }
	}
	
	/* convert forces to accelerations, giving new positions */
			
	FoundKE = 0.0;		/* and add up total KE */
			
	for (j=0; j<Nexatom; j++) {
	    /*
	      ff=vlen(force[j]);
	      fprintf(stderr, "--> Total force on atom %d is %.2f, displacement %f\n", j,
	      ff, ff*atom[j].massacc);
	    */
	    vmul2c(f,force[j],atom[j].massacc); // massacc = Dt*Dt/mass
				
	    if (vlen(f)>15.0) {
		fprintf(stderr, "High force %.2f in iteration %d\n",vlen(f), Iteration);
		pa(stderr, j);
	    }
				
	    vadd(new_positions[j],f);
	    vadd(average_positions[j],new_positions[j]);
				
	    vsub2(f, new_positions[j], positions[j]);
	    ff = vdot(f, f);
	    FoundKE += atom[j].energ * ff;
	}


	/* now the constraints */
	    
	//fprintf(stderr, "\njust before, positions=\n");
	//for (j=0;j<Nexatom;j++) pvt(positions[j]);
	    
	for (j=0;j<Nexcon;j++) {	/* for each constraint */
	    if (Constraint[j].type == CODEground) { /* welded to space */
		vsetc(foo,0.0);
		vsetc(q1,0.0);
		for (k=0; k<Constraint[j].natoms; k++) { // find center
		    vadd(foo,positions[Constraint[j].atoms[k]]);
		}
		vmulc(foo,1.0/Constraint[j].natoms);

		for (k=0; k<Constraint[j].natoms; k++) {
		    vsub2(rx,positions[Constraint[j].atoms[k]], foo);
		    v2x(bar,rx,force[Constraint[j].atoms[k]]);
		    vadd(q1,bar);
		}
		vmulc(q1,deltaTframe);
		vadd(Constraint[j].xdata, q1);
		Constraint[j].data++;

		for (k=0; k<Constraint[j].natoms; k++) {
		    new_positions[Constraint[j].atoms[k]] = positions[Constraint[j].atoms[k]];
		}
	    }
	    else if (Constraint[j].type == CODEmotor) { /* motor */
					
		mot=Constraint[j].motor;

		if (mot->speed != 0.0) {
		    sum_torque = 0.0;
					
		    /* input torque due to forces on each atom */
		    for (k=0; k<Constraint[j].natoms; k++) {
			a1 = Constraint[j].atoms[k];
			rx = vdif(positions[a1],mot->atocent[j]);
			f = vx(rx,force[a1]);
			ff = vdot(f, mot->axis);
			sum_torque += ff;
		    }
		    
		    //fprintf(stderr, "*** input torque %f\n", sum_torque);


		    omega = mot->theta - mot->theta0;
		    motorq = mot->stall - omega*mot->stall/(mot->speed);
		    theta = mot->theta + omega +
			mot->moment*(motorq + sum_torque);
  
		    /* theta_i+1 = 2theta_i - theta_i-1 + sum_torque + motorq
		       motorq = stall - omega*(stall/speed)
		       omega = (theta_i+1 - theta_i-1)/ 2Dt
		       solve for theta_i+1 -- preserves Verlet reversibility  */
		    /*
		      z = mot->moment;
		      m = - z * mot->stall / (2.0 *  mot->speed);
		      theta = (2.0*mot->theta - (1.0+m)*mot->theta0 +
		      z*(mot->stall + sum_torque))  / (1.0 - m);
		    */

		    // fprintf(stderr, "***  Theta = %f, %f, %f\n",
		    //          theta*1e5, mot->theta*1e5, mot->theta0*1e5);
		    
		    /* put atoms in their new places */
		    for (k=0; k<Constraint[j].natoms; k++) {
			a1 = Constraint[j].atoms[k];
			z = theta + mot->atang[k];
			vmul2c(v1, mot->roty, mot->radius[k] * cos(z));
			vmul2c(v2, mot->rotz, mot->radius[k] * sin(z));
			vadd2(new_positions[a1], v1, v2);
			vadd(new_positions[a1], mot->atocent[k]);
		    }
					
		    /* update the motor's position */
		    if (theta>Pi) {
			mot->theta0 = mot->theta-2.0*Pi;
			mot->theta = theta-2.0*Pi;
		    }
		    else {
			mot->theta0 = mot->theta;
			mot->theta = theta;
		    }
		    // data for printing speed trace
		    Constraint[j].data += omega * deltaTframe;
		    Constraint[j].temp += (motorq) * deltaTframe;
		}
	    }

	    else if (Constraint[j].type == CODEtemp) { // thermometer

		z=deltaTframe/(3*(1+Constraint[j].atoms[1]-
				  Constraint[j].atoms[0]));
		ff=0.0;
		for (a1 = Constraint[j].atoms[0];
		     a1 <= Constraint[j].atoms[1];
		     a1++) {
		    f = vdif(positions[a1],new_positions[a1]);
		    ff += vdot(f, f)*element[atom[a1].elt].mass;
		}
		ff *= Dx*Dx/(Dt*Dt) * 1e-27 / Boltz;
		Constraint[j].data += ff*z;
	    }

	    else if (Constraint[j].type == CODEstat) { // Langevin thermostat

		z=deltaTframe/(3*(1+Constraint[j].atoms[1]-
				  Constraint[j].atoms[0]));
		ke=0.0;

		for (a1 = Constraint[j].atoms[0];
		     a1 <= Constraint[j].atoms[1];
		     a1++) {
		    therm = sqrt((Boltz*Constraint[j].temp)/
				 (element[atom[a1].elt].mass * 1e-27))*Dt/Dx;
		    v1 = vdif(new_positions[a1],positions[a1]);
		    ff = vdot(v1, v1)*element[atom[a1].elt].mass;
		    vmulc(v1,1.0-Gamma);
		    v2= gxyz(G1*therm);
		    vadd(v1, v2);
		    vadd2(new_positions[a1],positions[a1],v1);

		    // add up the energy
		    ke += vdot(v1, v1)*element[atom[a1].elt].mass - ff;

		}
		ke *= 0.5 * Dx*Dx/(Dt*Dt) * 1e-27 * 1e18;
		Constraint[j].data += ke;

	    }
	    else if (Constraint[j].type == CODEangle) { // angle meter
		// better have 3 atoms exactly

		vsub2(v1,new_positions[Constraint[j].atoms[0]],
		      new_positions[Constraint[j].atoms[1]]);
		vsub2(v2,new_positions[Constraint[j].atoms[2]],
		      new_positions[Constraint[j].atoms[1]]);
		z=acos(vdot(v1,v2)/(vlen(v1)*vlen(v2)));

		Constraint[j].data = z;
	    }
	    else if (Constraint[j].type == CODEradius) { // radius meter
		// better have 2 atoms exactly

		vsub2(v1,new_positions[Constraint[j].atoms[0]],
		      new_positions[Constraint[j].atoms[1]]);

		Constraint[j].data = vlen(v1);
	    }
	}
	    
	// fprintf(stderr, "just after, new=\n");
	// for (j=0;j<Nexatom;j++) pvt(new_positions[j]);
	    
			
	tmp=old_positions; old_positions=positions; positions=new_positions; new_positions=tmp;
			
    } /* end of main loop */
	
    for (j=0; j<Nexatom; j++) {
	vmulc(average_positions[j],deltaTframe);
    }
	
}


/**
 */
void snapshot(int n) {
    int i,j;
    char c0, c1, c2;
    double xyz=1.0e-2; // .xyz files are in angstroms

    if (DumpAsText) {

        fprintf(outf, "%d\nFrame %d, Iteration: %d\n", Nexatom, n, Iteration);

        for (i=0; i<Nexatom; i++) {
            fprintf(outf, "%s %f %f %f\n", element[atom[i].elt].symbol,
                    average_positions[i].x*xyz, average_positions[i].y*xyz, average_positions[i].z*xyz);
        }
    }
    else {
        for (i=0, j=0; i<3*Nexatom; i+=3, j++) {
            ixyz[i+0] = (int)average_positions[j].x;
            ixyz[i+1] = (int)average_positions[j].y;
            ixyz[i+2] = (int)average_positions[j].z;
            c0=(char)(ixyz[i+0] - previxyz[i+0]);
            fwrite(&c0, sizeof(char), 1, outf);
            c1=(char)(ixyz[i+1] - previxyz[i+1]);
            fwrite(&c1, sizeof(char), 1, outf);
            c2=(char)(ixyz[i+2] - previxyz[i+2]);
            fwrite(&c2, sizeof(char), 1, outf);

            //fprintf(stderr, "%d %d %d\n", (int)c0, (int)c1, (int)c2);

        }
        temp = previxyz;
        previxyz = ixyz;
        ixyz = temp;

    }

    tracon(tracef);

    fflush(outf);

    // fprintf(stderr, "found Ke = %e\n",FoundKE);

}


static void min_debug(char *label, double rms, int frameNumber) 
{
    fprintf(stderr, "---------------- %s -- frame %d\nrms: %f\n", label, frameNumber, rms);
    printAllBonds(stderr);
}

static int interruptionWarning = 0;

/**
 */
void minshot(int final, double rms, double hifsq, int frameNumber, char *callLocation) {
    int i,j;
    char c0, c1, c2;
    double xyz=1.0e-2; // .xyz files are in angstroms

    if (DEBUG(D_MINIMIZE)) {
        min_debug(callLocation, rms, frameNumber);
    }

    if (DumpAsText) {

	if (final) {
	    fprintf(outf, "%d\nRMS=%f\n", Nexatom, rms);

	    for (i=0; i<Nexatom; i++) {
		fprintf(outf, "%s %f %f %f\n", element[atom[i].elt].symbol,
			positions[i].x*xyz, positions[i].y*xyz, positions[i].z*xyz);
	    }
	}
    }
    else {
        for (i=0, j=0; i<3*Nexatom; i+=3, j++) {
            ixyz[i+0] = (int)positions[j].x;
            ixyz[i+1] = (int)positions[j].y;
            ixyz[i+2] = (int)positions[j].z;
            c0=(char)(ixyz[i+0] - previxyz[i+0]);
            fwrite(&c0, sizeof(char), 1, outf);
            c1=(char)(ixyz[i+1] - previxyz[i+1]);
            fwrite(&c1, sizeof(char), 1, outf);
            c2=(char)(ixyz[i+2] - previxyz[i+2]);
            fwrite(&c2, sizeof(char), 1, outf);

            //fprintf(stderr, "%d %d %d\n", (int)c0, (int)c1, (int)c2);

        }
        temp = previxyz;
        previxyz = ixyz;
        ixyz = temp;

	fflush(outf);
    }

    fprintf(tracef,"%.2f %.2f\n", rms, sqrt(hifsq));
    if (final) {
        printf("final RMS gradient=%f after %d iterations\n", rms, frameNumber);
    }
    if (interrupted && !interruptionWarning) {
        WARNING("minimizer run was interrupted");
        interruptionWarning = 1;
    }
}

/* these are shared between minimizeSteepestDescent() and minimizeConjugateGradients() */
double sum_forceSquared;
double movcon = 4e-4;

/*
  Minimize via adaptive steepest descent.
  
  Will do a maximum of steepestDescentFrames iterations.  Returns true
  if rms_force has dropped below 50 pN before the iteration limit is
  reached.
*/
int
minimizeSteepestDescent(int steepestDescentFrames,
                        int *frameNumber)
{
    int i, j;
    struct xyz *tmp;
    struct xyz f; // force
    double last_sum_forceSquared;
    double rms_force;
    double max_forceSquared;
    double forceSquared;
    double movfac = 1.5;
    double sum_force_dot_old_force;
    double xxx, yyy;
    
    // 2 fixed steps to initialize
    for (i=0; i<2; i++) {
	max_forceSquared = 0.0;
	sum_forceSquared = 0.0;
	calcloop(1); // one iteration, do orion()
	for (j=0; j<Nexatom; j++) {
	    f = force[j];
	    old_force[j] = f;
	    forceSquared = vdot(f,f);
	    sum_forceSquared += forceSquared;
	    if (forceSquared>max_forceSquared) max_forceSquared = forceSquared;
	    vmulc(f, movcon);
	    vadd2(old_positions[j], positions[j], f);
	}
	tmp = old_positions; old_positions=positions; positions=tmp;
	rms_force = sqrt(sum_forceSquared/Nexatom);
    }
    minshot(0, rms_force, max_forceSquared, (*frameNumber)++, "1");

    // adaptive stepsize steepest descents until RMS gradient is under 50
    for (; *frameNumber < steepestDescentFrames && rms_force>50.0 && !interrupted;) {
	last_sum_forceSquared = sum_forceSquared;
	max_forceSquared = 0.0;
	sum_forceSquared = 0.0;
	sum_force_dot_old_force=0.0;
	calcloop(1);
	for (j=0; j<Nexatom; j++) {
	    f= force[j];
	    forceSquared = vdot(f,f);
	    if (forceSquared>max_forceSquared) max_forceSquared = forceSquared;
	    sum_forceSquared += forceSquared;
	    sum_force_dot_old_force += vdot(f,old_force[j]);
	}
	rms_force = sqrt(sum_forceSquared/Nexatom);

	minshot(0, rms_force, max_forceSquared, (*frameNumber)++, "2");
        
	xxx = sqrt(last_sum_forceSquared); // == previous rms_force * sqrt(Nexatom)
	yyy = sum_force_dot_old_force/xxx;
	if (yyy < (xxx - xxx/(movfac))) {
            movcon *= xxx/(xxx-yyy);
        } else {
            movcon *= movfac;
        }
        DPRINT(D_MINIMIZE, "xxx: %f yyy: %f movcon: %f\n", xxx, yyy, movcon);
        
	for (j=0; j<Nexatom; j++) {
	    f= force[j];
	    old_force[j] = f;
	    vmulc(f, movcon);
	    vadd2(old_positions[j], positions[j], f);
	}
	tmp = old_positions; old_positions=positions; positions=tmp;
    }
    if (rms_force <= 50.0) {
        return 1;
    } else {
	minshot(1, rms_force, max_forceSquared, (*frameNumber)++, "SDfinal");
        return 0;
    }
}

void minimizeConjugateGradients(int numFrames, int *frameNumber)
{
    int i, j, k;
    double forceSquared, max_forceSquared;
    double sum_old_force_squared;
    double last_sum_forceSquared;
    double sum_force_dot_old_force;
    double gamma; // = sum_forceSquared / last_sum_forceSquared
    double xxx, yyy, zzz;
    struct xyz f; // force
    struct xyz *tmp;
    double rms_force;
    double old_movcon = movcon;
    double movfac = 3.0;
    
    max_forceSquared = 0.0;
    last_sum_forceSquared = sum_forceSquared;
    sum_forceSquared = 0.0;
    calcloop(1);
    for (j=0; j<Nexatom; j++) {
	f= force[j];
	forceSquared = vdot(f,f);
	if (forceSquared>max_forceSquared) max_forceSquared = forceSquared;
	sum_forceSquared += forceSquared;
    }
    rms_force = sqrt(sum_forceSquared/Nexatom);

    // conjugate gradients for a while
    for (; (DumpAsText ? rms_force>1.0 : *frameNumber<numFrames) && !interrupted;) {
	//for (i=0; i<20 ;  i++) {
	minshot(0, rms_force, max_forceSquared, (*frameNumber)++, "3");
	gamma = sum_forceSquared/last_sum_forceSquared;
	// compute the conjugate direction 
	last_sum_forceSquared=sum_forceSquared;
	sum_old_force_squared=0.0;
	sum_force_dot_old_force=0.0;
	for (j=0; j<Nexatom; j++) {
	    vmul2c(f,old_force[j],gamma);
	    vadd(f,force[j]);
	    old_force[j]=f;
	    sum_old_force_squared += vdot(f,f);
	    sum_force_dot_old_force += vdot(force[j],old_force[j]);
	}
	tmp = old_positions; old_positions=positions; positions=tmp;
	xxx = sqrt(sum_old_force_squared);
	yyy = sum_force_dot_old_force/xxx;
	zzz = yyy;
        DPRINT(D_MINIMIZE, "xxx: %f yyy: %f\n", xxx, yyy);
	for (k=0; k<10 && yyy*yyy>1.0 && (DumpAsText || *frameNumber<numFrames) && !interrupted; k++) {
	    for (j=0; j<Nexatom; j++) {
		f=old_force[j];
		vmulc(f, movcon);
		vadd2(positions[j],old_positions[j], f);
	    }
	    sum_forceSquared = 0.0;
	    sum_force_dot_old_force=0.0;
	    calcloop(0);
	    for (j=0; j<Nexatom; j++) {
		f= force[j];
		forceSquared = vdot(f,f);
		if (forceSquared>max_forceSquared) max_forceSquared = forceSquared;
		sum_forceSquared += forceSquared;
		sum_force_dot_old_force += vdot(f,old_force[j]);
	    }
	    rms_force = sqrt(sum_forceSquared/Nexatom);
            /*
            minshot(0,rms_force, max_forceSquared, (*frameNumber)++, "4"); 
            */
	    yyy = sum_force_dot_old_force/xxx;
	    if (yyy<zzz-zzz/(movfac)) movcon *= zzz/(zzz-yyy);
	    else movcon *= movfac;
            DPRINT(D_MINIMIZE, "xxx: %f yyy: %f zzz: %f movcon: %f\n", xxx, yyy, zzz, movcon);
	}
	old_movcon=movcon;
	if (yyy<xxx-xxx/(movfac+1.0)) movcon *= xxx/(xxx-yyy)-1.0;
	else movcon *= movfac;
        DPRINT(D_MINIMIZE, "xxx: %f yyy: %f movcon: %f\n", xxx, yyy, movcon);
	for (j=0; j<Nexatom; j++) {
	    f= old_force[j];
	    vmulc(f, movcon);
	    vadd(positions[j], f);
	}
	if (movcon<0) movcon = old_movcon+movcon;
	max_forceSquared = 0.0;
	sum_forceSquared = 0.0;
	calcloop(0);
	for (j=0; j<Nexatom; j++) {
	    f= force[j];
	    forceSquared = vdot(f,f);
	    if (forceSquared>max_forceSquared) max_forceSquared = forceSquared;
	    sum_forceSquared += forceSquared;
	}
	rms_force = sqrt(sum_forceSquared/Nexatom);
    }
    minshot(1, rms_force, max_forceSquared, (*frameNumber)++, "final");
}

void minimize(int numFrames)
{
    int frameNumber;
    int steepestDescentFrames;
    
    frameNumber = 1;
    steepestDescentFrames = DumpAsText ? numFrames : numFrames / 2;

    /* turn off constraints --
       minimize is a one-shot run of the program */
    Nexcon=0;

    Temperature = 0.0;
    
    fprintf(tracef,"\n# rms force, high force\n");

    if (minimizeSteepestDescent(steepestDescentFrames, &frameNumber)) {
        minimizeConjugateGradients(numFrames, &frameNumber);
    } else {
        if (!interruptionWarning) {
            WARNING("partial minimization");
        }
    }
}

void SIGTERMhandler(int sig) 
{
    interrupted = 1;
}

#if 0
static void installSIGTERMhandler() 
{
    struct sigaction act;

    act.sa_handler = &SIGTERMhandler;
    sigemptyset(&act.sa_mask);
    act.sa_flags = 0;
    if (sigaction(SIGTERM, &act, NULL) < 0) {
        perror("sigaction()");
        exit(1);
    }
}
#endif

static void usage()
{
                
    fprintf(stderr, "command line parameters:\n\
   -dx -- dump, x= a: atoms; b: bonds; c: constraints\n\
   -n -- expect <number> of atoms\n\
   -m -- minimize the structure\n\
   -i -- number of iterations per frame\n\
   -f -- number of frames\n\
   -s -- timestep\n\
   -t -- temperature\n\
   -x -- write positions as (text) .xyz file(s)\n\
   -r -- repress frame numbers\n\
   -o -- output file name (otherwise same as input)\n\
   -q -- trace file name (otherwise trace)\n\
   -Dn -- turn on debugging flag n (see simulator.h)\n\
   filename -- if no ., add .mmp to read, .dpb to write\n");
    exit(0);
}


main(int argc,char **argv)
{
    int i, j, n;
    int da=0, db=0, dc=0, dw=0, mmpkey=0, dpbkey=0;
    struct xyz p, foo;
    double therm = 0.645;
	
    char buf[1024], *filename, *ofilename, *tfilename, *c;
	
    double x,y,z, end, theta;

    if (signal(SIGTERM, &SIGTERMhandler) == SIG_ERR) {
        perror("signal(SIGTERM)");
        exit(1);
    }

    maktab(uft1, uft2, uffunc, UFSTART, UFTLEN, UFSCALE);
	
    positions    =position_arrays;
    old_positions=position_arrays+NATOMS;
    new_positions=position_arrays+2*NATOMS;
	
    vsetc(Cog,0.0);
    vsetc(P,0.0);
    vsetc(Omega,0.0);
	
    filename = (char *)0;
    ofilename = (char *)0;
    tfilename = (char *)0;

    for (i=1; i<argc; i++) {

	if (argv[i][0] == '-') {
	    switch (argv[i][1]) {
	    case 'h':
                usage();
	    case 'd':
		if (argv[i][2]=='a') da = 1;
		if (argv[i][2]=='b') db = 1;
		if (argv[i][2]=='c') dc = 1;
		if (argv[i][2]=='w') dw = 1;
	    case 'n':
		n = atoi(argv[i]+2);
		if (n>NATOMS) {
		    fprintf(stderr, "n too high = %d\n",n);
		    exit(0);
		}
		break;
	    case 'm':
		ToMinimize=1;
		break;
	    case 'i':
		IterPerFrame = atoi(argv[i]+2);
		break;
	    case 'f':
		NumFrames = atoi(argv[i]+2);
		break;
	    case 's':
	        Dt = atof(argv[i]+2);
		break;
	    case 't':
		Temperature = atof(argv[i]+2);
		break;
	    case 'x':
		DumpAsText=1;
		break;
	    case 'r':
		PrintFrameNums=0;
		break;
	    case 'D':
		n = atoi(argv[i]+2);
                if (n < 32 && n >= 0) {
                    debug_flags |= 1 << n;
                }
		break;
        case 'o':
		ofilename=argv[i]+2;
		break;
	    case 'q':
		tfilename=argv[i]+2;
		break;
	    default:
		fprintf(stderr, "unknown switch %s\n",argv[i]+1);
	    }
	}	
	else {
	    filename = argv[i];
	}
    }

    if (!filename) {
        usage();
    }

    if (ToMinimize) printf("Minimize\n");

    if (strchr(filename, '.')) {
        sprintf(buf, "%s", filename);
    } else {
        sprintf(buf, "%s.mmp", filename);
    }

    if (! ofilename) {
	strcpy(OutFileName,buf);
	c=strchr(OutFileName, '.');
	if (c) {
            *c='\0';
        }
    } else {
        strcpy(OutFileName,ofilename);
    }
    
    if (! strchr(OutFileName, '.')) {
	if (DumpAsText) {
            strcat(OutFileName,".xyz");
        } else {
            strcat(OutFileName,".dpb");
        }
    }

    if (! tfilename) {
	strcpy(TraceFileName,buf);
	c=strchr(TraceFileName, '.');
	if (c) {
            *c='\0';
        }
    } else {
        strcpy(TraceFileName,tfilename);
    }
    
    if (! strchr(TraceFileName, '.')) {
        strcat(TraceFileName,".trc");
    }

    //IterPerFrame = IterPerFrame/innerIters;
    if (IterPerFrame <= 0) IterPerFrame = 1;

    bondinit();
    vdWsetup();
	

    filred(buf);
    
    
    orion();

    if (da) {
	fprintf(stderr, "%d atoms:\n",Nexatom);
	for (i=0; i<Nexatom; i++) pa(stderr, i);
    }
    if (db) {
	fprintf(stderr, "%d bonds:\n",Nexbon);
	for (i=0; i<Nexbon; i++) pb(stderr, i);
	fprintf(stderr, "%d torques:\n",Nextorq);
	for (i=0; i<Nextorq; i++) pq(stderr, i);
    }
    if (dw) {
	fprintf(stderr, "%d Waals:\n",vanderRoot);
	for (i=0; i<vanderRoot.fill; i++) pvdw(stderr, &vanderRoot,i);
    }
    if (dc) {
	fprintf(stderr, "%d constraints:\n",Nexcon);
	for (i=0; i<Nexcon; i++) pcon(stderr, i);
    }
    /*
    fprintf(stderr, " center of mass velocity: %f\n", vlen(vdif(CoM(positions),CoM(old_positions))));
    fprintf(stderr, " center of mass: %f -- %f\n", vlen(CoM(positions)), vlen(Cog));
    fprintf(stderr, " total momentum: %f\n",P);
    */
    tracef = fopen(TraceFileName, "w");
    if (!tracef) {
        perror(TraceFileName);
        exit(1);
    }
    printheader(tracef, filename, OutFileName, TraceFileName, 
                Nexatom, mmpkey, dpbkey, NumFrames, IterPerFrame, Temperature);

    if  (ToMinimize) {
	NumFrames = max(NumFrames,(int)sqrt((double)Nexatom));
	Temperature = 0.0;
    } else {
        headcon(tracef);
    }

    printf("iters per frame = %d\n",IterPerFrame /* *innerIters */ );
    printf("number of frames = %d\n",NumFrames);
    printf("timestep = %e\n",Dt);
    printf("temp = %f\n",Temperature);
    if (DumpAsText) printf("dump as text\n");

    printf("< %s  > %s\n", buf, OutFileName);

    printf("\nTotal Ke = %e\n",TotalKE);

    if (DumpAsText) {
        outf = fopen(OutFileName, "w");
        if (outf == NULL) {
            perror(OutFileName);
            exit(1);
        }
    } else {
	ixyz=ibuf1;
	previxyz=ibuf2;
	for (i=0, j=0; i<3*Nexatom; i+=3, j++) {
	    previxyz[i+0] = (int)positions[j].x;
	    previxyz[i+1] = (int)positions[j].y;
	    previxyz[i+2] = (int)positions[j].z;
	}
	outf = fopen(OutFileName, "wb");  
        if (outf == NULL) {
            perror(OutFileName);
            exit(1);
        }
	fwrite(&NumFrames, sizeof(int), 1, outf);
    }

    if  (ToMinimize) {
	minimize(NumFrames);
    }
    else {
	for (i=0; i<NumFrames; i++) {
	    if (PrintFrameNums) printf(" %d", i);
	    fflush(stdout);
	    if ((i & 15) == 15)
		if (PrintFrameNums) printf("\n");
	    calcloop(IterPerFrame);
	    snapshot(i);
	}

	/*  do the time-reversal (for debugging)
	tmp=positions; positions=new_positions; new_positions=tmp;

	for (i=0; i<NumFrames; i++) {
	    printf(" %d", i);
	    fflush(stdout);
	    if ((i & 15) == 15)
		printf("\n");
	    calcloop(IterPerFrame);
	    snapshot(i);
	}
	 */
    }

    fclose(outf);
    fclose(tracef);
    printf("\n");
	
    return 0;
	
}

/*
 * Local Variables:
 * c-basic-offset: 4
 * tab-width: 8
 * End:
 */

