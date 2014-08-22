import sys
import numpy as np
import matplotlib.pyplot as plt

# Global variables: responsive reserve ramp-related times
trrsnc = 0.5
t1rrsgn = 1.0
t2rrsgn = 16.0

# System parameters (syspar) come in the form:
# [LOSS, H, LOAD, RSPIN, RRSGN, RRSNC, PWIND, SIF, SEC]

# Get the frequency response over time
def freq_response(syspar):
    [LOSS, H, LOAD, RSPIN, RRSGN, RRSNC, PWIND, SIF, SEC] =\
	syspar
    time = [t*0.1 for t in range(SEC*10)]
    tspin = LOAD*(1-PWIND) + RSPIN + RRSGN # spin capacity
    f0M0 = 60.0/(2*H*tspin) # frequency equation coefficient
    SIL = 0.18*LOAD*PWIND*SIF
    SIH = 0.3*LOAD*PWIND*SIF
    freq = [f0M0*power_integral(t, syspar, SIL, SIH) \
	for t in time]
    nadir = min(freq)
    return (time, freq, nadir)

# Calculate frequency at any point in time
def power_integral(t, syspar, SIL, SIH):
    [LOSS, H, LOAD, RSPIN, RRSGN, RRSNC, PWIND, SIF, SEC] = \
	syspar
    pint = 0 # Power integral at time t
    # Response due to sudden loss at t=0
    if t >= 0:
	pint += -1*LOSS*t
    # Response due to RRSNC
    if t >= 0 and t <= trrsnc:
	pint += (RRSNC/(2*trrsnc))*(t**2)
    if t >  trrsnc:
	pint += RRSNC*(t - (trrsnc/2))
    # Response due to RRSGN
    if t >= t1rrsgn and t <= t2rrsgn:
	pint += (RRSGN/(2*(t2rrsgn-t1rrsgn)))*(t-t1rrsgn)**2
    if t > t2rrsgn:
	pint += RRSGN*(t - ((t1rrsgn + t2rrsgn)/2.0))
    # Response due to synthetic inertia (SI)
    if t >= 0 and t <= 3.0:
	pint += (SIH/6.0)*t**2
    if t > 3.0 and t <= 11.0:
	pint += SIH*(5.5 - (((t-11.0)**2)/16.0))
    if t > 11.0 and t <= 20.0:
	pint += 5.5*SIH - (SIL/18.0)*((t-11)**2)
    if t > 20.0 and t <= 80.0:
	pint += 5.5*SIH + SIL*(((t-80)**2/120)-34.5)
    if t > 80.0:
	pint += 5.5*SIH - 34.5*SIL
    # Return power integral
    return min(pint, 0.0)

def get_syspar(inp):
    # Default system parameters
    LOSS = 2.2e9
    H = 8.6 # Inertial constant [s]
    LOAD = 36.2e9 - LOSS # Generation to supply load [W]
    RSPIN = 4e9 # Spinning reserve [W]
    RRSGN = 1.75e9 # RRS - Generation [W]
    RRSNC = 1.05e9 # RRS - Non-controllable [W]
    PWIND = 0.0 # Percent of generation from wind
    SIF = 0.0 # Percent of wind with synthetic inertia
    SEC = 50 # Number of seconds to model
    # Replace system parameters with input
    for i in inp:
	if i[:5]=="LOSS=": LOSS=float(i[5:])
	if i[:2]=="H=": H=float(i[2:])
    	if i[:5]=="LOAD=": LOAD=float(i[5:]) - LOSS
	if i[:6]=="RSPIN=": RSPIN=float(i[6:])
	if i[:6]=="RRSGN=": RRSGN=float(i[6:])
	if i[:6]=="RRSNC=": RRSNC=float(i[6:])
	if i[:6]=="PWIND=": PWIND=float(i[6:])
	if i[:4]=="SIF=": SIF=float(i[4:])
	if i[:4]=="SEC=": SEC=float(i[4:])
    return [LOSS, H, LOAD, RSPIN, RRSGN, RRSNC, PWIND, \
	SIF, SEC]


if __name__ == "__main__":
    syspar = get_syspar(sys.argv[1:])
    (time, freq, nadir) = freq_response(syspar)
    print str(round(nadir+60,2))
    # Plot the response
    plt.plot(time, freq, 'b-', label="frequency response")
    plt.plot(time, [-0.7 for i in range(len(time))], 'r-', \
	label="UFLS threshold")
    plt.legend(loc = 'center right')
    plt.title("RRSGN=" + str(int(syspar[4]*1e-6))+\
	" MW, Other spinning reserve=" + \
	str(int(syspar[3]*1e-6)) + \
	" MW, \nGeneration from wind=" + \
	str(round(syspar[6]*100,2)) + \
	"%, Fraction of wind with synthetic inertia=" + \
	str(round(syspar[7]*100,2))+'%', size=10)
    plt.xlabel("Time [seconds]")
    plt.ylabel("Frequency deviation from 60Hz [Hz]")
    plt.show()

