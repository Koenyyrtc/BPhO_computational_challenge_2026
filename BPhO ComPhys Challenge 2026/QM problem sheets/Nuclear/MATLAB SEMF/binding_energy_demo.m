%binding_energy_demo
% Example calculation using (i) NUBASE data (ii) liquid drop model
%
% LAST UPDATED by Andy French February 2019
%
% Fission reaction:  U-235 + n -> Ba-141 + Kr-92 +3n
% Fusion reaction: H-2 + H-3 -> He-4 + n

function binding_energy_demo

%% INPUTS %%

%Graph fontsize
fsize = 18;

%%

%% EXAMPLE CALCULATION %%

disp(' ')
disp(' **** Nuclear Fission demo: U-235 + n -> Ba-141 + Kr-92 +3n ****')
disp(' ')

[B_MeV_nubase_U235,M_u_nubase_U235,B_MeV_model_U235,M_u_model_U235] =...
    B_and_mass(92,235);
[B_MeV_nubase_Ba141,M_u_nubase_Ba141,B_MeV_model_Ba141,M_u_model_Ba141] =...
    B_and_mass(56,141);
[B_MeV_nubase_Kr92,M_u_nubase_Kr92,B_MeV_model_Kr92,M_u_model_Kr92] =...
    B_and_mass(36,92);

%Difference in binding energy /MeV
dB_MeV_model = B_MeV_model_Kr92 + B_MeV_model_Ba141 - B_MeV_model_U235;
dB_MeV_exp = B_MeV_nubase_Kr92 + B_MeV_nubase_Ba141 - B_MeV_nubase_U235;
disp([' Energy released during fission (NUBASE) = ',num2str(dB_MeV_exp),'MeV' ])
disp([' Energy released during fission (Liquid Drop) = ',num2str(dB_MeV_model),'MeV' ])
disp(' ');

disp(' **** Nuclear Fusion demo: H-2 + H-3 -> He-4 + n ****')
disp(' ')

[B_MeV_nubase_D,M_u_nubase_D,B_MeV_model_D,M_u_model_D] =...
    B_and_mass(1,2);
[B_MeV_nubase_T,M_u_nubase_T,B_MeV_model_T,M_u_model_T] =...
    B_and_mass(1,3);
[B_MeV_nubase_He4,M_u_nubase_He4,B_MeV_model_He4,M_u_model_He4] =...
    B_and_mass(2,4);

%Difference in binding energy /MeV
dB_MeV_model = B_MeV_model_He4 - B_MeV_model_D - B_MeV_model_T;
dB_MeV_exp = B_MeV_nubase_He4 - B_MeV_nubase_D - B_MeV_nubase_T;
disp([' Energy released during fusion (NUBASE) = ',num2str(dB_MeV_exp),'MeV' ])
disp([' Energy released during fusion (Liquid Drop) = ',num2str(dB_MeV_model),'MeV' ])
disp(' ');

%%

%% BINDING ENERGY PER NUCLEON PLOT %%

%Plot binding energy per nucleon (b /MeV) vs number of nucleons (A)
load nubase;
figure('name','binding energy per nucleon','color',[1 1 1]);
plot(A,B_MeV_per_nucleon,'r+'); hold on;
[B_MeV_model,M_u_model] = liquid_drop(Z,A);
plot(A,B_MeV_model./A,'b+');
xlabel('Atomic mass number A','fontsize',fsize);
ylabel('Binding energy per nucleon /MeV','fontsize',fsize);
title('Binding energy per nucleon /MeV','fontsize',fsize);
legend({'NUBASE','Liquid Drop'},'fontsize',fsize,'location','southeast');
set(gca,'fontsize',fsize);
ylim([0,9]);
grid on;
box on;
print( gcf, 'binding energy per nucleon.png','-dpng','-r300' );

%Plot shaded surface of binding energy per nucleon vs atomi number and
%neutron number
clf;
hold on;
interp_colormap(500);
caxis([0,9]);
for n=1:length(A)
    [R,G,B] = RGB_from_colormap( B_MeV_per_nucleon(n),0,9);
    if ~isnan(R)
        plot( Z(n), A(n)-Z(n), '.','color',[R,G,B] );
    end
end
axis equal;
xlim([0,120])
ylim([0,200]);
xlabel('Atomic number Z','fontsize',fsize);
ylabel('Neutron number A-Z','fontsize',fsize);
title('Binding energy per nucleon /MeV','fontsize',fsize);
set(gca,'fontsize',fsize);
grid on;
box on;
print( gcf, 'binding energy per nucleon N vs Z.png','-dpng','-r300' );

%Plot shaded surface of binding energy per nucleon vs atomi number and
%neutron number
clf;
hold on;
Z = linspace(0,120,500);
N = linspace(0,200,500);
[Z,N] = meshgrid(Z,N);
A = N+Z;
[B_MeV_model,M_u_model] = liquid_drop(Z,A);
surf( Z,N,B_MeV_model./A,B_MeV_model./A );
shading interp
caxis([0,9]);
colorbar('fontsize',fsize);
axis equal;
xlim([0,120])
ylim([0,200]);
xlabel('Atomic number Z','fontsize',fsize);
ylabel('Neutron number A-Z','fontsize',fsize);
title('Binding energy per nucleon /MeV','fontsize',fsize);
set(gca,'fontsize',fsize);
grid on;
box on;
print( gcf, 'binding energy per nucleon model N vs Z.png','-dpng','-r300' );
close(gcf);

%%

%Mass and binding energy for an element z,a
function [B_MeV_nubase,M_u_nubase,B_MeV_model,M_u_model] = B_and_mass(z,a)
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
disp( [' ',nuclide{i}] )
[B_MeV_model,M_u_model] = liquid_drop(z,a);
disp([' NUBASE: B = ',num2str(B_MeV_nubase),'MeV, M = ',num2str(M_u_nubase),'u']);
disp([' Liquid drop: B = ',num2str(B_MeV_model),'MeV, M = ',num2str(M_u_model),'u']);
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

%%

%interp_colormap
% Function which interpolates current colourmap to yield better graduated
% shading. N is number of possible colours.
function interp_colormap(N)

%Get current colourmap
map = colormap;

%Initialise new colormap
new_map = ones(N,3);

%Get size of current colormap and initalise red,green,blue vectors
dim = size(map);
R = ones(1,dim(1));
G = ones(1,dim(1));
B = ones(1,dim(1));
RR = ones(1,N);
GG = ones(1,N);
BB = ones(1,N);

%Populate these with current colormap
R(:) = map(:,1);
G(:) = map(:,2);
B(:) = map(:,3);

%Interpolate to yield new colour map
x = linspace( 1, dim(1), N );
RR = interp1( 1:dim(1), R, x );
GG = interp1( 1:dim(1), G, x );
BB = interp1( 1:dim(1), B, x );
new_map(:,1) = RR(:);
new_map(:,2) = GG(:);
new_map(:,3) = BB(:);

%Set colormap to be new map
colormap( new_map );

%%

%RGB_from_colormap
function [R,G,B] = RGB_from_colormap(x,xmin,xmax)

%Get size of current colormap and initalise red,green,blue vectors
map = colormap;
dim = size(map);
red = ones(1,dim(1));
green = ones(1,dim(1));
blue = ones(1,dim(1));

%Populate these with current colormap
red(:) = map(:,1); green(:) = map(:,2); blue(:) = map(:,3);

%Interpolate to yield RGB colours
x = (x-xmin)/(xmax-xmin);
xx = linspace( 0, 1, dim(1) );
x(x>1) = 1;
x(x<0) = 0;
R = interp1( xx, red, x );
G = interp1( xx, green, x );
B = interp1( xx, blue, x );

%End of code