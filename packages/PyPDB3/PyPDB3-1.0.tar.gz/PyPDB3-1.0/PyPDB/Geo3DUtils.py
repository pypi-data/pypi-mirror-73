
import string
import sys
import os
import copy
import math
import gzip
import random

def randomDirection():
    """
    Draw a random direction using M. Petitjean sphere approach.
    """
    U = [0., 0., 0.]
    compteur=0
    
    N = 2.
    while (N>1.) and (compteur < 1000):
        U[1]=-1+random.random()*2 # reel compris entre -1 et 1
        U[2]=-1+random.random()*2
        U[0]=-1+random.random()*2
        N = U[0] * U[0] + U[1] * U[1] + U[2] * U[2]
    
    if compteur >= 1000:
        return None;
  
    N = math.sqrt(N);
    U[0] /= N;
    U[1] /= N;
    U[2] /= N;
    return U;

def identityRotMat():
    RM = [ [1., 0., 0., 0.],
           [0., 1., 0., 0.],
           [0., 0., 1., 0.],
           [0., 0., 0., 0.]]
    return RM

def rndRotMat(A, min_angle, max_angle):
    """
    build a transformation matrix corresponding to a rotation centered on A.
    Angles MUST be in radians
    """
    D = randomDirection()
    if D is None:
        return identityRotMat
    angle_value =  (random.random() * (max_angle - min_angle))  + min_angle
    B = [A[0]+D[0], A[1]+D[1], A[2]+D[2] ]
    
    return MkArbitraryAxisRotMat4x4(A, B, angle_value)


def MkArbitraryAxisRotMat4x4(A, B, angle):
    cosa = math.cos(angle)
    sina = math.sin(angle)
    
    rx = B[0] - A[0]
    ry = B[1] - A[1]
    rz = B[2] - A[2]
    lnorme = math.sqrt(rx*rx + ry*ry + rz*rz)
    rx /= lnorme
    ry /= lnorme
    rz /= lnorme
    
    rx2 = rx*rx
    ry2 = ry*ry
    rz2 = rz*rz
    rxry = rx*ry
    rxrz = rx*rz
    ryrz = ry*rz
    rxry1mcosa = rxry * (1. - cosa)
    rxrz1mcosa = rxrz * (1. - cosa)
    ryrz1mcosa = ryrz * (1. - cosa)
    
    matrice = identityRotMat()
    matrice[0][0] = rx2 + (1. - rx2) * cosa
    matrice[1][0] = rxry1mcosa - rz * sina
    matrice[2][0] = rxrz1mcosa + ry * sina
    
    matrice[0][1] = rxry1mcosa + rz * sina
    matrice[1][1] = ry2 + (1. - ry2) * cosa
    matrice[2][1] = ryrz1mcosa - rx * sina
    
    matrice[0][2] = rxrz1mcosa - ry * sina
    matrice[1][2] = ryrz1mcosa + rx * sina
    matrice[2][2] = rz2 + (1. - rz2) * cosa
    
    matrice[3][0] =  A[0] * (1 - matrice[0][0]) - A[1] * matrice[1][0] - A[2] * matrice[2][0]
    matrice[3][1] = -A[0] * matrice[0][1] + A[1] * (1 - matrice[1][1]) - A[2] * matrice[2][1]
    matrice[3][2] = -A[0] * matrice[0][2] - A[1] * matrice[1][2] + A[2] * (1 - matrice[2][2])
    
    matrice[0][3] = matrice[1][3] = matrice[2][3] = 0.
    matrice[3][3] = 1.
    
    return matrice

def transform(x,y,z, TM):
    xo = x * TM[0][0] + y * TM[1][0] + z * TM[2][0] + TM[3][0]; 
    yo = x * TM[0][1] + y * TM[1][1] + z * TM[2][1] + TM[3][1]; 
    zo = x * TM[0][2] + y * TM[1][2] + z * TM[2][2] + TM[3][2]; 
    return xo, yo, zo
        
def vecteur(x1,y1,z1,x2,y2,z2):
	return x2-x1, y2-y1, z2-z1

def distance(x1,y1,z1,x2,y2,z2):
	dx = x2-x1
	dy = y2-y1
	dz = z2-z1
	d = dx*dx+dy*dy+dz*dz
	return math.sqrt(d)

def dxdydz(x1,y1,z1,x2,y2,z2):
    dx = x2-x1
    dy = y2-y1
    dz = z2-z1
    return dx, dy, dz

def mixtproduct(x1,y1,z1,x2,y2,z2,x3,y3,z3):
	x = y1 * z2 - z1 * y2
	y = z1 * x2 - x1 * z2
	z = x1 * y2 - y1 * x2
	n = math.sqrt(x*x + y*y + z*z)
	x = x / n
	y = y / n
	z = z / n

	return x * x3 + y * y3 + z * z3

def RTOD(x):
	return x * 180.0 / 3.14159265358979323846

def DTOR(x):
	return x * 3.14159265358979323846 / 180.0

def valence(x1,y1,z1, x2,y2,z2, x3,y3,z3):
    """
    return valence angle (degrees)
    """
    dx = x1 - x2
    dy = y1 - y2
    dz = z1 - z2
    rd =  math.sqrt(dx * dx + dy * dy + dz * dz);

    bx = x3 - x2
    by = y3 - y2
    bz = z3 - z2
    rb =  math.sqrt(bx * bx + by * by + bz * bz)
    rr = (dx * bx + dy * by + dz * bz) / (rd * rb)

    return RTOD( math.acos(rr))


def dihedral(x1,y1,z1, x2,y2,z2, x3,y3,z3, x4,y4,z4):

    #	print x1,y1,z1, x2,y2,z2, x3,y3,z3, x4,y4,z4
	ab_x = (x2 - x1)
	ab_y = (y2 - y1)
	ab_z = (z2 - z1)
	bc_x = (x3 - x2)
	bc_y = (y3 - y2)
	bc_z = (z3 - z2)
	cd_x = (x4 - x3)
	cd_y = (y4 - y3)
	cd_z = (z4 - z3)

	d012  = ab_x * bc_x + ab_y * bc_y + ab_z * bc_z
	d123  = cd_x * bc_x + cd_y * bc_y + cd_z * bc_z
	d0123 = ab_x * cd_x + ab_y * cd_y + ab_z * cd_z

	d01   = ab_x * ab_x + ab_y * ab_y + ab_z * ab_z
	d12   = bc_x * bc_x + bc_y * bc_y + bc_z * bc_z
	d23   = cd_x * cd_x + cd_y * cd_y + cd_z * cd_z

	num = d012 * d123 - d12 * d0123
	den = (d01*d12 - d012*d012)*(d12*d23 - d123*d123)
	arccos = num / math.sqrt(den)

	if arccos > 1.:
		arccos = 1.

	if arccos < -1.:
		arccos = -1.

	RS = math.acos(arccos)

	RS1 = cd_x * (ab_y * bc_z - ab_z * bc_y) + \
	      cd_y * (bc_x * ab_z - ab_x * bc_z) + \
	      cd_z * (ab_x * bc_y - ab_y * bc_x)

	if RS1 > 0.:
		return RTOD(RS)
	else:
		return - RTOD(RS)

def single_peptide2World(ca, n, c, atm):
        """
        convert local crd to global ones attached to the reference build upon Ca, N, C
        Local reference is:
        Z = CaN ^ CaC
        Y = - (CaN + CaC)
        X = Y ^ Z
        here atm is a tuple of x,y,z
        """
        # /* -------------------------------------------------------local reference */
        x0 = ca[0]
        y0 = ca[1]
        z0 = ca[2]
        xa = n[0] - x0    # /* CaN */
        ya = n[1] - y0
        za = n[2] - z0
        ra = math.sqrt(xa * xa + ya * ya + za * za)
        xb = c[0] - x0    # /* CaC  */
        yb = c[1] - y0
        zb = c[2] - z0
        rb = math.sqrt(xb * xb + yb * yb + zb * zb)
        tx = ya * zb - za * yb
        ty = za * xb - xa * zb
        tz = xa * yb - ya * xb
        rt = math.sqrt(tx * tx + ty * ty + tz * tz)
        cx = tx / rt
        cy = ty / rt
        cz = tz / rt      # /* C = CaN ^ CaC normalise  = axe Z */
        tx = -xa / ra - xb / rb
        ty = -ya / ra - yb / rb
        tz = -za / ra - zb / rb
        rt = math.sqrt(tx * tx + ty * ty + tz * tz)
        bx = tx / rt
        by = ty / rt
        bz = tz / rt      # /* B = CaN - CaC, normalise = axe Y */
        tx = by * cz - bz * cy
        ty = bz * cx - bx * cz
        tz = bx * cy - by * cx
        rt = math.sqrt(tx * tx + ty * ty + tz * tz)
        ax = tx / rt
        ay = ty / rt
        az = tz / rt     # /* B ^ C, normalise = axe X (proche CaN) */

        
        # print ax, ay, az
        # print bx, by, bz
        # print cx, cy, cz
        # print x0, y0, z0

        # /* ------------------------------- transform coordinates */
        lx, ly, lz = atm[0], atm[1], atm[2]
        wx = ax * lx + bx * ly + cx * lz + x0
        wy = ay * lx + by * ly + cy * lz + y0
        wz = az * lx + bz * ly + cz * lz + z0
        # print "After Reference change:"
        # print wx, wy, wz
        return wx, wy, wz

def peptide2World(ca, n, c, atms):
    """
    convert local crd to global ones attached to the reference build upon Ca, N, C
    Local reference is:
    Z = CaN ^ CaC
    Y = - (CaN + CaC)
    X = Y ^ Z
    """
    # /* -------------------------------------------------------local reference */
    x0 = ca[0]
    y0 = ca[1]
    z0 = ca[2]
    xa = n[0] - x0    # /* CaN */
    ya = n[1] - y0
    za = n[2] - z0
    ra = math.sqrt(xa * xa + ya * ya + za * za)
    xb = c[0] - x0    # /* CaC  */
    yb = c[1] - y0
    zb = c[2] - z0
    rb = math.sqrt(xb * xb + yb * yb + zb * zb)
    tx = ya * zb - za * yb
    ty = za * xb - xa * zb
    tz = xa * yb - ya * xb
    rt = math.sqrt(tx * tx + ty * ty + tz * tz)
    cx = tx / rt
    cy = ty / rt
    cz = tz / rt      # /* C = CaN ^ CaC normalise  = axe Z */
    tx = -xa / ra - xb / rb
    ty = -ya / ra - yb / rb
    tz = -za / ra - zb / rb
    rt = math.sqrt(tx * tx + ty * ty + tz * tz)
    bx = tx / rt
    by = ty / rt
    bz = tz / rt      # /* B = CaN - CaC, normalise = axe Y */
    tx = by * cz - bz * cy
    ty = bz * cx - bx * cz
    tz = bx * cy - by * cx
    rt = math.sqrt(tx * tx + ty * ty + tz * tz)
    ax = tx / rt
    ay = ty / rt
    az = tz / rt     # /* B ^ C, normalise = axe X (proche CaN) */

    
    # print ax, ay, az
    # print bx, by, bz
    # print cx, cy, cz
    # print x0, y0, z0

    # /* ------------------------------- transform coordinates */
    for atm in atms:
        if atm.atmName() in ["N","CA","C","O","OXT","OT1","OT2","H1","H2","H3"]:
            continue
        lx, ly, lz = atm.xyz()
        # print "Will transform:"
        # print lx, ly, lz

        wx = ax * lx + bx * ly + cx * lz + x0
        wy = ay * lx + by * ly + cy * lz + y0
        wz = az * lx + bz * ly + cz * lz + z0
        # print "After Reference change:"
        # print wx, wy, wz
        atm.setcrds(wx, wy, wz)
    return atms

def world2Peptide(ca, n, c, atms, scOnly = True):
    """
    convert global crd to local ones attached to the reference build upon Ca, N, C
    Local reference is:
    Z = CaN ^ CaC
    Y = - (CaN + CaC)
    X = Y ^ Z
    """

    # /* -------------------------------------------------------local reference */
    x0 = ca[0];
    y0 = ca[1];
    z0 = ca[2];
    xa = n[0] - x0;
    ya = n[1] - y0;
    za = n[2] - z0;
    ra = math.sqrt(xa * xa + ya * ya + za * za);
    xb = c[0] - x0;
    yb = c[1] - y0;
    zb = c[2] - z0;
    rb = math.sqrt(xb * xb + yb * yb + zb * zb);
    tx = ya * zb - za * yb;
    ty = za * xb - xa * zb;
    tz = xa * yb - ya * xb;
    rt = math.sqrt(tx * tx + ty * ty + tz * tz);
    cx = tx / rt;
    cy = ty / rt;
    cz = tz / rt;
    tx = -xa / ra - xb / rb;
    ty = -ya / ra - yb / rb;
    tz = -za / ra - zb / rb;
    rt = math.sqrt(tx * tx + ty * ty + tz * tz);
    bx = tx / rt;
    by = ty / rt;
    bz = tz / rt;
    tx = by * cz - bz * cy;
    ty = bz * cx - bx * cz;
    tz = bx * cy - by * cx;
    rt = math.sqrt(tx * tx + ty * ty + tz * tz);
    ax = tx / rt;
    ay = ty / rt;
    az = tz / rt;

    # print ax, ay, az
    # print bx, by, bz
    # print cx, cy, cz
    # print x0, y0, z0
    
    # /* ------------------------------- transform coordinates */
    for atm in atms:
        if scOnly and (atm.atmName() in ["N","CA","C","O","OXT","OT1","OT2","H1","H2","H3"]):
            # print "Skipping for \"%s\"" % atm.atmName()
            continue
        lx, ly, lz = atm.xyz()
        # print "Will transform"
        # print lx, ly, lz

        lx -= x0;
        ly -= y0;
        lz -= z0;

        # print "Origin change:"
        # print lx, ly, lz
        
        px = lx*ax+ly*ay+lz*az;
        py = lx*bx+ly*by+lz*bz;
        pz = lx*cx+ly*cy+lz*cz;

        # print "Reference change:"
        # print px, py, pz
        oldcrds = atm.crds()
        atm.setcrds(px, py, pz)
        # print "%s old crds: %s new crds: %s" % (atm.atmName(), oldcrds, atm.crds())
        # print atm
    return atms

def single_world2Peptide(ca, n, c, atm):
    """
    convert global crd to local ones attached to the reference build upon Ca, N, C
    Local reference is:
    Z = CaN ^ CaC
    Y = - (CaN + CaC)
    X = Y ^ Z
    """

    # /* -------------------------------------------------------local reference */
    x0 = ca[0];
    y0 = ca[1];
    z0 = ca[2];
    xa = n[0] - x0;
    ya = n[1] - y0;
    za = n[2] - z0;
    ra = math.sqrt(xa * xa + ya * ya + za * za);
    xb = c[0] - x0;
    yb = c[1] - y0;
    zb = c[2] - z0;
    rb = math.sqrt(xb * xb + yb * yb + zb * zb);
    tx = ya * zb - za * yb;
    ty = za * xb - xa * zb;
    tz = xa * yb - ya * xb;
    rt = math.sqrt(tx * tx + ty * ty + tz * tz);
    cx = tx / rt;
    cy = ty / rt;
    cz = tz / rt;
    tx = -xa / ra - xb / rb;
    ty = -ya / ra - yb / rb;
    tz = -za / ra - zb / rb;
    rt = math.sqrt(tx * tx + ty * ty + tz * tz);
    bx = tx / rt;
    by = ty / rt;
    bz = tz / rt;
    tx = by * cz - bz * cy;
    ty = bz * cx - bx * cz;
    tz = bx * cy - by * cx;
    rt = math.sqrt(tx * tx + ty * ty + tz * tz);
    ax = tx / rt;
    ay = ty / rt;
    az = tz / rt;

    # print ax, ay, az
    # print bx, by, bz
    # print cx, cy, cz
    # print x0, y0, z0
    
    # /* ------------------------------- transform coordinates */
    lx, ly, lz = atm[0], atm[1], atm[2]
    lx -= x0;
    ly -= y0;
    lz -= z0;
    px = lx*ax+ly*ay+lz*az;
    py = lx*bx+ly*by+lz*bz;
    pz = lx*cx+ly*cy+lz*cz;

    return px, py, pz


def zmirror(atms):
    for atm in atms:
        if atm.atmName() in ["N","CA","C","O","OXT","OT1","OT2","H1","H2","H3"]:
            continue
        lx, ly, lz = atm.xyz()
        lz = -lz
        atm.setcrds(lx, ly, lz)
    return atms

def D_aminoacid(res):
    """
    
    """
    atms = res.atms
    world2Peptide(atms[atms.CApos()].xyz(), atms[atms.Npos()].xyz(), atms[atms.Cpos()].xyz(), atms)
    atms = zmirror(atms)
    res.atms = peptide2World(atms[atms.CApos()].xyz(), atms[atms.Npos()].xyz(), atms[atms.Cpos()].xyz(), atms)
    return res

## def oneHMMGeo(theCAs, aCA):
## 	CA1x, CA1y, CA1z = atmCrds(theCAs[aCA])
## 	CA2x, CA2y, CA2z = atmCrds(theCAs[aCA+1])
## 	CA3x, CA3y, CA3z = atmCrds(theCAs[aCA+2])
## 	CA4x, CA4y, CA4z = atmCrds(theCAs[aCA+3])
## 	d1 = distance(CA1x, CA1y, CA1z, CA3x, CA3y, CA3z)
## 	d2 = distance(CA1x, CA1y, CA1z, CA4x, CA4y, CA4z)
## 	d3 = distance(CA2x, CA2y, CA2z, CA4x, CA4y, CA4z)
## 	x1, y1, z1 = vecteur(CA1x, CA1y, CA1z, CA2x, CA2y, CA2z)
## 	x2, y2, z2 = vecteur(CA2x, CA2y, CA2z, CA3x, CA3y, CA3z)
## 	x3, y3, z3 = vecteur(CA3x, CA3y, CA3z, CA4x, CA4y, CA4z)
## 	d4 = mixtproduct(x1, y1, z1, x2, y2, z2, x3, y3, z3)
## 	d5 = distance(CA1x, CA1y, CA1z, CA2x, CA2y, CA2z)
## 	d6 = distance(CA2x, CA2y, CA2z, CA3x, CA3y, CA3z)
## 	d7 = distance(CA3x, CA3y, CA3z, CA4x, CA4y, CA4z)
## 	return d1,d2,d3,d4,d5,d6,d7

## def HMMGeo(theCAs, theId):
## 	for aCA in range(0,len(theCAs)-3):
## 		d1,d2,d3,d4,d5,d6,d7 = oneHMMGeo(theCAs, aCA)
## 		print "%s %10.6lf %10.6lf %10.6lf %10.6lf %10.6lf %10.6lf %10.6lf %3d %s" % (resNum(theCAs[aCA]), d1,d2,d3,d4,d5,d6,d7, len(theCAs)-3, theId)

## PDBDATADIR = "/raid5/HMM/data/"

## if __name__=='__main__':
## 	useChain = ' '
## 	if len(sys.argv[1]) == 5:
## 		useChain = sys.argv[1][4]
## 	theTrace = pdbTrace(PDBDATADIR+sys.argv[1]+".pdb", useChain, 1)
## 	HMMGeo(theTrace, sys.argv[1])


def sOPEPCentroid(ca, n, c, rTpe):
        """
Return the crds of the sOPEP SC centroid, given the crds of n, ca, c and residue type

from Geo3DUtils import *

ca= [69.442,  74.383,  -1.181]
n = [68.141,  73.784,  -0.971]
c = [70.457,  73.260,  -1.069]
sc = [ -0.25542 , 2.46877 , 1.87947]
single_peptide2World(ca, n, c, sc)  # 69.817  77.135   0.225

sOPEPCentroid(ca, n, c, 8) # 69.817  77.135   0.225

import PyPDB.Geo3DUtils as geo
ca= [80.502,  76.889,   3.322]
n = [81.297,  76.189,   4.324]
c = [79.092,  76.312,   3.244]
geo.sOPEPCentroid(ca, n, c, 18) # 81.837  77.653   0.915
        """
        gSCStdBC_new = [
                [ -0.31378 , 0.67543 , 0.95910],       # /* ALA */ 
                [ -0.17496 , 1.32270 , 1.42172],       # /* CYS */ 
                [ -0.18009 , 1.57201 , 1.44001],       # /* ASP */ 
                [ -0.26304 , 2.09135 , 1.79080],       # /* GLU */ 
                [ -0.33210 , 2.08028 , 1.55238],       # /* PHE */ 
                [ -0.62244 , 0.16476 , 0.24186],       # /* GLY */ 
                [ -0.35577 , 2.04482 , 1.56483],       # /* HIS */ 
                [ -0.21642 , 1.60142 , 1.59292],       # /* ILE */ 
                [ -0.25542 , 2.46877 , 1.87947],       # /* LYS */ 
                [ -0.27380 , 1.99989 , 1.30147],       # /* LEU */ 
                [ -0.20793 , 2.16418 , 1.59493],       # /* MET */ 
                [ -0.24557 , 1.61219 , 1.42074],       # /* ASN */ 
                [ -1.16055 , 0.50625 , 1.30015],       # /* PRO */ 
                [ -0.29135 , 2.15120 , 1.70894],       # /* GLN */ 
                [ -0.26575 , 2.72122 , 2.32715],       # /* ARG */ 
                [ -0.02157 , 0.91606 , 1.50897],       # /* SER */ 
                [ -0.13072 , 1.16220 , 1.49624],       # /* THR */ 
                [  0.37182 , 0.94921 , 1.02156],       # /* VAL */ 
                [ -0.06457 , 2.37604 , 1.58512],       # /* TRP */ 
                [ -0.28932 , 2.26972 , 1.59971]]       # /* TYR */ 

        # print gSCStdBC_new[rTpe]
        return single_peptide2World(ca, n, c, gSCStdBC_new[rTpe])

def rmsd(sys1, sys2):
    """
    rmsd between 2 lists of crds
    """
    if len(sys1) != len(sys2):
        print("rmsd: Size Error (%d vs %d)" % (len(sys1), len(sys2)))
        sys.exit(0)
    somme = 0
    # print sys1, sys2
    for i in range(len(sys1)):
        somme += (sys1[i][0]-sys2[i][0])*(sys1[i][0]-sys2[i][0])
        somme += (sys1[i][1]-sys2[i][1])*(sys1[i][1]-sys2[i][1])
        somme += (sys1[i][2]-sys2[i][2])*(sys1[i][2]-sys2[i][2])
    somme /= len(sys1)
    return math.sqrt(somme)
