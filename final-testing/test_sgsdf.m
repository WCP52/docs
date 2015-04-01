
clear
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%P. A. Gorry, "General Least-Squares Smoothing and Differentiation by the Convolution (Savitzky-Golay) Method," 
%Analytical Chemistry, vol. 62, pp. 570-573, 1990.
%Table I

xn=2;x=-xn:xn;n=2;dn=0;hs=[];
for x0=-xn:xn
    h=sgsdf(x,n,dn,x0,1);
    hs=[hs h'];
end

hs=[sym(-xn:xn);hs];
hs=[[0;(sym(-2:2))'] hs];

disp('====================================================================================================');
disp('  P. A. Gorry, "General Least-Squares Smoothing and Differentiation by the Convolution (Savitzky-Golay) Method,"'); 
disp('  Analytical Chemistry, vol. 62, pp. 570-573, 1990.');
disp('====================================================================================================');
disp('----Table I----');
disp(sprintf('Point Number = %d  Polynomial Degree = %d  Differentiation Degree = %d',xn*2+1,n,dn));
disp(hs)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xn=3;x=-xn:xn;n=2;dn=0;hs=[];
for x0=-xn:xn
    h=sgsdf(x,n,dn,x0,1);
    hs=[hs h'];
end

hs=[sym(-xn:xn);hs];
hs=[[0;(sym(-3:3))'] hs];
disp(sprintf('Point Number = %d  Polynomial Degree = %d  Differentiation Degree = %d',xn*2+1,n,dn));
disp(hs)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xn=2;x=-xn:xn;n=2;dn=1;hs=[];
for x0=-xn:xn
    h=sgsdf(x,n,dn,x0,1);
    hs=[hs h'];
end

hs=[sym(-xn:xn);hs];
hs=[[0;(sym(-2:2))'] hs];
disp(sprintf('Point Number = %d  Polynomial Degree = %d  Differentiation Degree = %d',xn*2+1,n,dn));
disp(hs)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xn=3;x=-xn:xn;n=2;dn=1;hs=[];
for x0=-xn:xn
    h=sgsdf(x,n,dn,x0,1);
    hs=[hs h'];
end

hs=[sym(-xn:xn);hs];
hs=[[0;(sym(-3:3))'] hs];
disp(sprintf('Point Number = %d  Polynomial Degree = %d  Differentiation Degree = %d',xn*2+1,n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%P. A. Gorry, "General Least-Squares Smoothing and Differentiation by the Convolution (Savitzky-Golay) Method," 
%Analytical Chemistry, vol. 62, pp. 570-573, 1990.
%Table II

xn=2;x=-xn:xn;n=3;dn=0;hs=[];
for x0=-xn:xn
    h=sgsdf(x,n,dn,x0,1);
    hs=[hs h'];
end

hs=[sym(-xn:xn);hs];
hs=[[0;(sym(-2:2))'] hs];
disp('----Table II----');
disp(sprintf('Point Number = %d  Polynomial Degree = %d  Differentiation Degree = %d',xn*2+1,n,dn));
disp(hs)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xn=3;x=-xn:xn;n=3;dn=0;hs=[];
for x0=-xn:xn
    h=sgsdf(x,n,dn,x0,1);
    hs=[hs h'];
end

hs=[sym(-xn:xn);hs];
hs=[[0;(sym(-3:3))'] hs];
disp(sprintf('Point Number = %d  Polynomial Degree = %d  Differentiation Degree = %d',xn*2+1,n,dn));
disp(hs)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xn=2;x=-xn:xn;n=3;dn=1;hs=[];
for x0=-xn:xn
    h=sgsdf(x,n,dn,x0,1);
    hs=[hs h'];
end

hs=[sym(-xn:xn);hs];
hs=[[0;(sym(-2:2))'] hs];
disp(sprintf('Point Number = %d  Polynomial Degree = %d  Differentiation Degree = %d',xn*2+1,n,dn));
disp(hs)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xn=3;x=-xn:xn;n=3;dn=1;hs=[];
for x0=-xn:xn
    h=sgsdf(x,n,dn,x0,1);
    hs=[hs h'];
end

hs=[sym(-xn:xn);hs];
hs=[[0;(sym(-3:3))'] hs];
disp(sprintf('Point Number = %d  Polynomial Degree = %d  Differentiation Degree = %d',xn*2+1,n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%P. A. Gorry, "General Least-Squares Smoothing and Differentiation by the Convolution (Savitzky-Golay) Method," 
%Analytical Chemistry, vol. 62, pp. 570-573, 1990.
%Table III

n=2;dn=0;hs=[];
hs=sym(zeros(21,9));
for xn=2:10
    x=-xn:xn;
    x0=-xn;    
    h=sgsdf(x,n,dn,x0,1);
    hs(11-xn:11+xn,10-xn+1)=h';
end

hs=[sym((10:-1:2)*2+1);hs];
hs=[[0;(sym(-10:10))'] hs];
disp('----Table III----');
disp(sprintf('Initial Point  Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%P. A. Gorry, "General Least-Squares Smoothing and Differentiation by the Convolution (Savitzky-Golay) Method," 
%Analytical Chemistry, vol. 62, pp. 570-573, 1990.
%Table IV

n=2;dn=1;hs=[];
hs=sym(zeros(21,9));
for xn=2:10
    x=-xn:xn;
    x0=-xn;    
    h=sgsdf(x,n,dn,x0,1);
    hs(11-xn:11+xn,10-xn+1)=h';
end

hs=[sym((10:-1:2)*2+1);hs];
hs=[[0;(sym(-10:10))'] hs];
disp('----Table IV----');
disp(sprintf('Initial Point  Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%P. A. Baedecker, "Comments on Least-Square Polynomial Filters for Initial Point and Slope Estimation," 
%Analytical Chemistry, vol. 57, pp. 1477-1479, 1985.
%Talbe I

n=2;dn=0;hs=[];
hs=zeros(21,9);
for xn=2:10
    x=0:2*xn;
    x0=0;    
    h=sgsdf(x,n,dn,x0,0);
    hs(1:2*xn+1,xn-2+1)=h';
end

hs=([5:2:21;hs]);
hs=[[0;(0:20)'] hs];
disp('====================================================================================================');
disp('  P. A. Baedecker, "Comments on Least-Square Polynomial Filters for Initial Point and Slope Estimation," '); 
disp('  Analytical Chemistry, vol. 57, pp. 1477-1479, 1985.');
disp('====================================================================================================');
disp('----Table I----');
disp(sprintf('Initial Point  Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%P. A. Baedecker, "Comments on Least-Square Polynomial Filters for Initial Point and Slope Estimation," 
%Analytical Chemistry, vol. 57, pp. 1477-1479, 1985.
%Talbe II

n=2;dn=1;hs=[];
hs=zeros(21,9);
for xn=2:10
    x=1:(2*xn+1);
    x0=1;    
    h=sgsdf(x,n,dn,x0,0);
    hs(1:2*xn+1,xn-2+1)=h';
end

hs=([5:2:21;hs]);
hs=[[0;(0:20)'] hs];
disp('----Table II----');
disp(sprintf('Initial Point  Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%A. Savitzky and M. J. E. Golay, "Smoothing and Differentiation of Data by Simplified Least Squares Procedures," 
%Analytical Chemistry, vol. 36, pp. 1627-1639, 1964.
%J. Steinier, Y. Termonia, and J. Deltour, "Comments on Smoothing and Differentiation of Data by Simplified Least Square Procedures,"
%Analytical Chemistry, vol. 44, pp. 1906-1909, 1972.
%Table I

n=3;dn=0;x0=0;hs=[];
hs=sym(zeros(25,11));
for xn=2:12
    x=-xn:xn;
    h=sgsdf(x,n,dn,x0,1);
    hs(13-xn:13+xn,12-xn+1)=h';
end

hs=[sym((12:-1:2)*2+1);hs];
hs=[[0;(sym(-12:12))'] hs];
disp('====================================================================================================');
disp('  A. Savitzky and M. J. E. Golay, "Smoothing and Differentiation of Data by Simplified Least Squares Procedures," '); 
disp('  Analytical Chemistry, vol. 36, pp. 1627-1639, 1964.');
disp('  J. Steinier, Y. Termonia, and J. Deltour, "Comments on Smoothing and Differentiation of Data by Simplified Least Square Procedures," '); 
disp('  Analytical Chemistry, vol. 44, pp. 1906-1909, 1972.');
disp('====================================================================================================');
disp('----Table I----');
disp(sprintf('Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%A. Savitzky and M. J. E. Golay, "Smoothing and Differentiation of Data by Simplified Least Squares Procedures," 
%Analytical Chemistry, vol. 36, pp. 1627-1639, 1964.
%J. Steinier, Y. Termonia, and J. Deltour, "Comments on Smoothing and Differentiation of Data by Simplified Least Square Procedures,"
%Analytical Chemistry, vol. 44, pp. 1906-1909, 1972.
%Table II
n=6;dn=1;x0=0;hs=[];
hs=sym(zeros(25,10));
for xn=3:12
    x=-xn:xn;
    h=sgsdf(x,n,dn,x0,1);
    hs(13-xn:13+xn,12-xn+1)=h';
end

hs=[sym((12:-1:3)*2+1);hs];
hs=[[0;(sym(-12:12))'] hs];
disp('----Table II----');
disp(sprintf('Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%A. Savitzky and M. J. E. Golay, "Smoothing and Differentiation of Data by Simplified Least Squares Procedures," 
%Analytical Chemistry, vol. 36, pp. 1627-1639, 1964.
%J. Steinier, Y. Termonia, and J. Deltour, "Comments on Smoothing and Differentiation of Data by Simplified Least Square Procedures,"
%Analytical Chemistry, vol. 44, pp. 1906-1909, 1972.
%Table III
n=4;dn=2;x0=0;hs=[];
hs=sym(zeros(25,10));
for xn=3:12
    x=-xn:xn;
    h=sgsdf(x,n,dn,x0,1);
    hs(13-xn:13+xn,12-xn+1)=h';
end

hs=[sym((12:-1:3)*2+1);hs];
hs=[[0;(sym(-12:12))'] hs];
disp('----Table III----');
disp(sprintf('Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%A. Savitzky and M. J. E. Golay, "Smoothing and Differentiation of Data by Simplified Least Squares Procedures," 
%Analytical Chemistry, vol. 36, pp. 1627-1639, 1964.
%J. Steinier, Y. Termonia, and J. Deltour, "Comments on Smoothing and Differentiation of Data by Simplified Least Square Procedures,"
%Analytical Chemistry, vol. 44, pp. 1906-1909, 1972.
%Table IV
n=6;dn=3;x0=0;hs=[];
hs=sym(zeros(25,10));
for xn=3:12
    x=-xn:xn;
    h=sgsdf(x,n,dn,x0,1);
    hs(13-xn:13+xn,12-xn+1)=h';
end

hs=[sym((12:-1:3)*2+1);hs];
hs=[[0;(sym(-12:12))'] hs];
disp('----Table IV----');
disp(sprintf('Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%A. Savitzky and M. J. E. Golay, "Smoothing and Differentiation of Data by Simplified Least Squares Procedures," 
%Analytical Chemistry, vol. 36, pp. 1627-1639, 1964.
%J. Steinier, Y. Termonia, and J. Deltour, "Comments on Smoothing and Differentiation of Data by Simplified Least Square Procedures,"
%Analytical Chemistry, vol. 44, pp. 1906-1909, 1972.
%Table V
n=4;dn=4;x0=0;hs=[];
hs=sym(zeros(25,10));
for xn=3:12
    x=-xn:xn;
    h=sgsdf(x,n,dn,x0,1);
    hs(13-xn:13+xn,12-xn+1)=h';
end

hs=[sym((12:-1:3)*2+1);hs];
hs=[[0;(sym(-12:12))'] hs];
disp('----Table V----');
disp(sprintf('Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%A. Savitzky and M. J. E. Golay, "Smoothing and Differentiation of Data by Simplified Least Squares Procedures," 
%Analytical Chemistry, vol. 36, pp. 1627-1639, 1964.
%J. Steinier, Y. Termonia, and J. Deltour, "Comments on Smoothing and Differentiation of Data by Simplified Least Square Procedures,"
%Analytical Chemistry, vol. 44, pp. 1906-1909, 1972.
%Table VI
n=6;dn=5;x0=0;hs=[];
hs=sym(zeros(25,10));
for xn=3:12
    x=-xn:xn;
    h=sgsdf(x,n,dn,x0,1);
    hs(13-xn:13+xn,12-xn+1)=h';
end

hs=[sym((12:-1:3)*2+1);hs];
hs=[[0;(sym(-12:12))'] hs];
disp('----Table VI----');
disp(sprintf('Polynomial Degree = %d  Differentiation Degree = %d',n,dn));
disp(hs)
