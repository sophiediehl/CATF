import sys
import numpy as np
import matplotlib.pyplot as plt
import frequency_response as fr

# Find the ancillary service combination that avoids
# under-frequency load shedding at lowest cost
def lowest_cost_soln(syspar, rspins, rrsgns, sibool):
    [LOSS, H, LOAD, RSPIN, RRSGN, RRSNC, PWIND, SIF, SEC] =\
        syspar
    o = []
    costs = []
    for rspin in rspins:
      syspar[3] = rspin
      for rrsgn in rrsgns:
	syspar[4] = rrsgn
	# SIF cannot be so high as to cause freq rebound
	if sibool: 
	  sifmax = min(1.0, \
		(rrsgn + RRSNC - LOSS)/(LOAD*PWIND*0.18))
	  sifs=[i*(sifmax/20.0) for i in range(21)]
	else: sifs = [0.0]
	for sif in sifs:
	  syspar[7] = sif
	  (time, freq, nadir) = fr.freq_response(syspar)
	  if nadir > -0.7: # Avoids UFLS
	    o.append(syspar[:])
	    costs.append(cost(syspar))
    if len(costs) == 0: return (0, [0]*9)
    mincost = min(costs)
    bestsyspar = o[costs.index(mincost)]
    return (mincost, bestsyspar)

# Calculate cost for comparison's sake
def cost(syspar):
    [LOSS, H, LOAD, RSPIN, RRSGN, RRSNC, PWIND, SIF, SEC] =\
        syspar
    capacity = LOAD + RSPIN + RRSGN
    gencost = capacity*1e-6*get_LMP(capacity)
    rrsgncost = RRSGN*1e-6*get_rrsprice(RRSGN)
    return gencost + rrsgncost

# Generation cost in $/(MW*hour) for a given capacity
def get_LMP(capacity):
    x = capacity*1e-6
    result = 4.4481*(1e-13)*x**3  \
	- 1.4382*(1e-8)*x**2 \
	- 9.4676*(1e-4)*x \
	+ 56.662
    return max(24.24, result)

# Price in $/(MW*h) for a given rrsgn level
def get_rrsprice(rrsgn):
    x = rrsgn*1e-6
    result = 0.20914*np.exp(0.0013231*x)
    return result

def printsyspar(syspar):
    #[LOSS, H, LOAD, RSPIN, RRSGN, RRSNC, PWIND, SIF, SEC]
    print "LOSS = " + str(syspar[0]*1e-6) + " MW"
    print "RSPIN = " + str(syspar[3]*1e-6) + " MW"
    print "RRSGN = " + str(syspar[4]*1e-6) + " MW"
    print "PWIND = " + str(syspar[6])
    print "SIF = " + str(syspar[7])

def report_solution(pwind, sibool):
    print ""
    syspar = fr.get_syspar(["PWIND="+str(pwind)])
    rspins = [4e9 + i*0.1e9 for i in range(81)]
    rrsgns = [1.75e9 + i*0.05e9 for i in range(81)]
    (mincost, bestsyspar) = \
      lowest_cost_soln(syspar, rspins, rrsgns, sibool)
    (time, freq, nadir) = fr.freq_response(bestsyspar)
    print "nadir: "+str(round(nadir + 60,2))
    print "cost: "+ str(round(mincost,2))
    printsyspar(bestsyspar)
    print ""


if __name__ == "__main__":
    winds = [0.05*i for i in range(11,16)] # Up to 75% wind
    for pwind in winds:
	report_solution(pwind, True)
	report_solution(pwind, False)



