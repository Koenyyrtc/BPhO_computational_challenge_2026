%Bcalc
% Binding energy and mass calculator using (i) NUBASE data (ii) liquid drop
% model. Syntax: Bcalc(z,a)
%
% LAST UPDATED by Andy French January 2020

%Mass and binding energy for an element z,a
function Bcalc(z,a)
load nubase

%Atomic mass unit /kg
u = 1.66053886e-27;

%Speed of light /ms^-1
c = 299792458;

%Charge of electron /C
qe = 1.60217662e-19;

%Find B and M values using Z,A
i = find( ( A==a ) & ( Z==z ) );
i = i(1);
B_MeV_nubase = B_MeV(i);
M_u_nubase = (M_MeV(i)*1e6*qe/(c^2))/u;

%Display calculations
disp(' ')
disp( [' ',nuclide{i}] )
[B_MeV_model,M_u_model] = liquid_drop(z,a);
disp([' NUBASE:        B = ',num2str(B_MeV_nubase),'MeV,   B/A = ',...
    num2str(B_MeV_nubase/a),'MeV,   M = ',num2str(M_u_nubase),'u']);
disp([' Liquid drop:   B = ',num2str(B_MeV_model),'MeV,   B/A = ',...
    num2str(B_MeV_model/a),'MeV,   M = ',num2str(M_u_model),'u']);
disp(' ');

%%

%Determine Binding Energy and mass of nucleus from liquid drop model
function [B_MeV,M_u] = liquid_drop(Z,A)

%Constants /MeV from https://en.wikipedia.org/wiki/Semi-empirical_mass_formula
a_v = 15.56;
a_s = 17.81;
a_c = 0.711;
a_a = 23.702;
a_p = 34;

%Atomic mass unit /kg
u = 1.66053886e-27;

%Speed of light /ms^-1
c = 299792458;

%Charge of electron /C
qe = 1.60217662e-19;

%Proton mass /u
mp = 1.007276466879;

%Neutron mass /u
mn = 1.00866491588;

%Neutron number
N = A - Z;

%Pairing term
dA = zeros(size(A));
both_even = find(( rem(Z,2)==0 ) & ( rem(N,2)==0 ) );
both_odd = find(( rem(Z,2)~=0 ) & ( rem(N,2)~=0 ) );
dA(both_even) = a_p*A(both_even).^(-3/4);
dA(both_odd) = -a_p*A(both_odd).^(-3/4);

%Compute Binding Energy /MeV
B_MeV = a_v*A - a_s*A.^(2/3) -a_c*(Z.^2)./(A.^(1/3)) - a_a*((N-Z).^2)./A + dA;

%Compute nuclear mass /u
M_u = Z*mp + N*mn - ( B_MeV*1e6*qe/(c^2) )/u ;

%End of code