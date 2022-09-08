A synthetic generator capability curve can be formulated by making three assumptions. 
The first assumption is that the capability curve is the intersection of three circles. 
The second assumption is that the minimum and maximum real and reactive power limits 
that are given create a rectangular capability “box” that fits completely within the 
actual generator capability curve. The third assumption is that the maximum rated 
apparent power output is greater than the maximum apparent power output as calculated 
from the maximum real and reactive power output as defined in the synthetic case. 
The three circles that makeup the generator capability curve are the armature current limit, 
the field current limit, and the end-region heating limit. 

The armature current limit can be modeled by Equation 1 below [1].

P^2+Q^2≤(S_max )^2             	            	                (1)

In Equation 1, P is the real power output, Q is the reactive power output, and S_max 
is the maximum apparent power output calculated from Equation 2 below.

〖P_max〗^2+〖Q_max〗^2=(S_max )^2   			                      (2)

In Equation 2, P_max and Q_max are the maximum real and reactive power defined 
in the synthetic case. 
The field current limit is modeled by a circle with a center on the Q-axis below the P-axis. 
Three equations are used to find the field current limit. Equation 3 is the circle that 
models the field current limit [1]. Equation 4 finds the center of that circle [1]. 
Finally, Equation 5 finds the radius of that circle [1].

P^2+(Q-Q_0^field )^2≤(r^field )^2                                                 (3)

Q_0^field=(Q_(max,t)^2-S_max^2)/2(Q_(max,t)-S_max √(1-〖pf〗_lagging^2 ))         (4)

r^field=Q_(max,t)-Q_0^field                                                      (5)

In the above three equations,  Q_0^field is the center of the circle, r^field is the radius 
of the circle, P is the real power output of the generator, Q is the reactive power output 
of the generator, S_max is the maximum apparent power output as calculated in Equation 2, 
Q_(max,t) is the maximum reactive power as calculated in Equation 6 below, and finally,
〖 pf〗_lagging is the minimum power factor as calculated from Equation 7 below.

Q_(max,t)=√(S_rated^2-〖P_max〗^2 )                                               (6)

〖pf〗_lagging=  P_max/S_max                                                      (7)

In the above two equations, S_rated is the maximum rated apparent power output of the generator, 
and the other variables are the same as defined above. The maximum rated apparent power output 
of the generator was chosen because Equation 4 is found using trigonometry. 
In this trigonometric problem there is not enough information to solve it without knowing Q_(max,t). 
It is known that Q_(max,t) should be larger than Q_max. The maximum rated apparent power is larger 
than the maximum apparent power calculated in Equation 2 which means Equation 6 will give us a 
reasonable value for Q_(max,t). From [2], Equation 8 below is the actual center of the circle.

Q_0^field=-(V_t^2)/X_s                                                            (8)

In Equation 8, V_t is the armature terminal voltage and X_s is the synchronous reactance. 
For synthetic cases, Equation 8 will likely yield unrealistic results because the generator 
parameters are synthetic. As such, they are not necessarily related to the generator capability curve 
in the way that they should be. For this reason, it is preferred to use 
Equation 6 to obtain a realistic value for Q_(max,t).  
The end-region heating limit is modeled by a circle with a center on the Q-axis above the P-axis. 
Three equations are used to find the end-region heating limit. Equation 9 is the circle that models 
the end-region heating limit [1]. Equation 10 finds the center of that circle [1]. 
Finally, Equation 11 finds the radius of that circle [1].

P^2+(Q-Q_0^end )^2≤(r^end )^2                                                    (9)

Q_0^end=(Q_(min,t)^2-S_max^2)/2(Q_(min,t)+S_max √(1-〖pf〗_leading^2 ))          (10)

r^end=Q_0^end-Q_(min,t)                                                          (11)

In the three equations above, Q_0^end is the center of the circle that lies on the Q-axis, 
r^end is the radius of the circle, Q_(min,t) is the actual minimum reactive power output as determined 
by Equation 12 below, and 〖pf〗_leading is the minimum power factor as determined by Equation 13 below.

Q_(min,t)=√(S_rated^2-(〖pf〗_leading∙S_max )^2 )                                      (12)

〖pf〗_leading=  P_max/√(P_(max )^2+Q_min^2 )                                                        (13)

The previous definitions of the parameters in the above two equations apply. The center of the circle 
that sweeps out the arc that models the end-region heating limit, Q_0^end, was found using trigonometry. 
As with the field current limit, there is not enough information to solve it without knowing Q_(min,t). 
Equation 12 produces a reasonable value for Q_(min,t) by the same reasoning that Equation 6 
produces a reasonable value for Q_(max,t). Equation 14 below is the actual value for Q_(min,t) [3].

Q_(min,t)=SCR/2+1/(2∙X_e )                                                      (14)

In Equation 14, SCR is the short circuit ratio, and X_e is the external impedance [3]. 
For the same reason Equation 8 could not be used to determine the center of the field current 
limit circle, Equation 14 cannot be used. In synthetic cases, specific generator parameters are 
also synthetic. Thus, they do not necessarily relate to the generator capability curve in the way 
that they should. Using Equation 14 will often yield unrealistic generator capability curves 
because of this problem.

References
[1] 	D.K. Molzahn, Z.B. Friedman, B.C. Lesieutre, C.L. DeMarco, and M.C. Ferris, "Estimation 
        of Constraint Parameters in Optimal Power Flow Data Sets," 47th North American Power 
        Symposium (NAPS), 4-6 October 2015.

[2]  	P. Kundur, N. Balu, and M. Lauby, Power System Stability and Control. McGraw-hill New York, 1994.

[3] 	S. B. Farnham and R. W. Swarthout, "Field Excitation in Relation to Machine and System 
        Operation [includes discussion]," in Transactions of the American Institute of Electrical Engineers. 
        Part III: Power Apparatus and Systems, vol. 72, no. 6, pp. 1215-1223, Dec. 1953, doi: 10.1109/AIEEPAS.1953.4498759.
