      program sigma_v

*****************
*****************
*Author : Christian Carles

*Last update : 2021

*this program calculates for each time step,in radial bins,
*the velocity dispersion of gas particles. It does so in 
*cylindircal coordinates (r, theta, z) but it could easily 
*be changed to x, y, x. 

*it output sigma_v.out, with 1 line = 1 bin at 1 time :

*1 :  timestep
*2 :  central radius of the bin
*3 :  width of the bin
*4 :  # of the bin
*5 :  # of gas particles in the bin
*6 :  sigma_r of particles in bin
*7 :  sigma_t of particles in bin
*8 :  sigma_z of particles in bin

*the lines to create sigma_time.out are included but commented.
*sigma_time.out instead outputs for each time step the sigma values
*of the 10 first bins.



*This program is to be used with the following GCDP output ASCII files :
* tzstep.dat, gXXXXXX, sXXXXXX.


*use nbin and rmax to control number and spread of bins
*******************

*parameters and arrays for data
      implicit double precision (a-h,m,o-z)
      parameter (nmax=1000000)
      parameter (rmax=10.)
      parameter (nbin=50)
      parameter (pi=3.14159265359)

      character filename *7

*arrays of all particles
      dimension rs(nmax,3), ms(nmax), rg(nmax,3), mg(nmax), dist(nmax),
     +          vg(nmax,3)
*arrays for each bin      
      dimension  mgR(nbin), ngR(nbin), aveV(nbin,3),
     +           sigmaV(nbin,4)

      integer count(nbin)
      integer flagfld
      integer N_dumps
      open(unit=9,file='tzstep.dat',status='old')
      open(unit=11,file='sigma_vgc.out',status='unknown')
*      open(unit=12,file='sigma_time.out',status='unknown')
      read(9,9000) dummyc
 9000 format(a3)


*******************

*Read number of time steps , not counting first line
      tmax=1000
      N_dumps = 0
      DO i=1,int(tmax)
      READ(9,*,IOSTAT=ios) junk
      IF (ios /= 0) EXIT
      N_dumps= N_dumps + 1
      ENDDO
      REWIND(9)
*write nuber of steps
      write(6,2301) N_dumps
 2301 format(3x,'Total numbr of simulated steps = ',i6)
      read(9,9000) dummyc


**************************

*Start big loop over all time dumps. l marks the dump number
      do l=1,N_dumps
           read(9,*,end=98) num, t
*WRITE at witch step we are on (6=teal)
           write(6,2300) num, t
 2300      format(3x,'Working on dump ',i6,5x,'Time = ',1pe13.6)

* get the good filename for dump
           if(num.lt.10) then
                write(filename,8000) num
 8000           format('s00000',i1)
           else if(num.lt.100) then
                write(filename,8001) num
 8001           format('s0000',i2)
           else if(num.lt.1000) then
                write(filename,8002) num
 8002           format('s000',i3)
           else if(num.lt.10000) then
                write(filename,8003) num
 8003           format('s00',i4)
           else if(num.lt.100000) then
                write(filename,8004) num
 8004           format('s0',i5)
           else
                write(filename,8005) num
 8005           format('s',i6)
           endif


****************************


*open the star file, read position, mass, number of particles  

        open(unit=1,file=filename,status='old')
        ns=0
        do i=1,nmax
           read(1,*,end=98) (rs(i,j),j=1,3), (dummy,j=1,3), ms(i)
           ns=ns+1
        enddo
   98   close(unit=1)


* Open the gas file of our dump, read position, velocity, mass
* particles. ABCD are placeholders to some day merge different codes
*together. Luckly GCD+ already handles vr, v theta and vz
        filename(1:1)='g'
        open(unit=1,file=filename,status='old')
        ng=0
        do i=1,nmax
             read(1,*,end=99) x, y, z, vx, vy,vz, m, A, B, 
     +                       (dummy, j=1,10), flagflg, (dummy,j=1,3), 
     +                       C, D,(dummy,j=1,5),vph,vr 
*Feedback particles (flag not = 0) are stars not gas 
             if(flagflg.eq.0) then
                  ng=ng+1
*units of r in kpc, mass in M sun
                  rg(ng,1)=x
                  rg(ng,2)=y
                  rg(ng,3)=z
                  mg(ng)=m
****cylindircal coords****
                  d = SQRT(x*x+y*Y)
*vg 1 is v_radial
                  vg(ng,1)=(x*vx+y*vy)/d
*vg 2 is v _t
                  vg(ng,2)=(x*vy-y*vx)/d
*vg 3 is vz
                  vg(ng,3)=vz
********cartesial coords****
*vg 1 is vx
*                  vg(ng,1)=vx
*vg 2 is vy
*                  vg(ng,2)=vy
*vg 3 is vz
*                  vg(ng,3)=vz

              else
                  ns=ns+1
                  rs(ns,1)=x
                  rs(ns,2)=y
                  rs(ns,3)=z
                  ms(ns)=m
            endif
        enddo
   99   close(unit=1)

****************************

*Reset all radial values to 0 for the new timestep
        dr=rmax/float(nbin)
        do index=1,nbin
            aveV(index,1)=0.
            aveV(index,2)=0.
            aveV(index,3)=0.
            sigmaV(index,1)=0. 
            sigmaV(index,2)=0.
            sigmaV(index,3)=0.
            sigmaV(index,4)=0.
*            rp(index)=0.
            mgR(index)=0.
            ngR(index)=0.
        end do 

**************************
*calculate mass center in stars in case galaxy moves
      xcm=0.
      ycm=0.
      zcm=0.
      mstot=0.
      do i=1,ns
        xcm=xcm+rs(i,1)*ms(i)
        ycm=ycm+rs(i,2)*ms(i)
        zcm=zcm+rs(i,3)*ms(i)
        mstot=mstot+ms(i)
      enddo
      xcm=xcm/mstot
      ycm=ycm/mstot
      zcm=zcm/mstot

*loop over gas to attribute index
      do i=1,ng
        index=int(sqrt((rg(i,1)-xcm)**2+(rg(i,2)-ycm)**2)/dr)+1
*Add particle info to it's index. trow data over nbin
*aveV is going to become average velocity later.
*for now it's only sum of all the velocities.
        if (index.le.nbin) then
            ngR(index)=ngR(index)+1.0
            mgR(index)=mgR(index)+mg(i)
            aveV(index,1)=aveV(index,1)+vg(i,1)
            aveV(index,2)=aveV(index,2)+vg(i,2)
            aveV(index,3)=aveV(index,3)+vg(i,3)
        end if
      end do

********************************


*Loop over indexes to calculate average
      do index=1,nbin
*calculate average in each index

       aveV(index,1)=aveV(index,1)/ngR(index)
       aveV(index,2)=aveV(index,2)/ngR(index)
       aveV(index,3)=aveV(index,3)/ngR(index)
      end do

*loop over gas again to calculate sigma
*is there a smarter way to do this ? it seems dumb to re-pass
*all data, but I have not taken time to think about it.

      do i=1,ng
        index=int(sqrt((rg(i,1)-xcm)**2+(rg(i,2)-ycm)**2)/dr)+1

*calculate sum(Xi-Xmoy)**2
         if (index.le.nbin) then
           sigmaV(index,1)=sigmaV(index,1)+(vg(i,1)-aveV(index,1))**2
           sigmaV(index,2)=sigmaV(index,2)+(vg(i,2)-aveV(index,2))**2
           sigmaV(index,3)=sigmaV(index,3)+(vg(i,3)-aveV(index,3))**2
         end if
       end do
*loop over indexes to write down results.
      do index=1,nbin
*finish calculating sigma by diving by the number of particles
       sigmaV(index,1)=sqrt(sigmaV(index,1)/(ngR(index)-1.))
       sigmaV(index,2)=sqrt(sigmaV(index,2)/(ngR(index)-1.))
       sigmaV(index,3)=sqrt(sigmaV(index,3)/(ngR(index)-1.))
       sigmaV(index,4)=sqrt(sigmaV(index,1)**2+sigmaV(index,2)**2
     +                 +sigmaV(index,3)**2)

       r1=float(index-1)*dr
       r=r1+0.5*dr
*write down in sigma_v like this
*
      write(11,3001) t, r, dr,index, ngR(index),
     +               sigmaV(index,1), sigmaV(index,2),
     +               sigmaV(index,3),sigmaV(index,4)
 3001         format(3(2x,1pe13.6),2(2x,i7),4(2x,1pe13.6)) 
      enddo
*For sigma_time, dont forget to open it 
*      write(12,3002) t,sigmaV(1,1), sigmaV(1,2),sigmaV(1,3),sigmaV(1,4),
*     +                sigmaV(2,1), sigmaV(2,2), sigmaV(2,3),sigmaV(2,4),
*     +                sigmaV(3,1), sigmaV(3,2), sigmaV(3,3),sigmaV(3,4),
*     +                sigmaV(4,1), sigmaV(4,2), sigmaV(4,3),sigmaV(4,4),
*     +                sigmaV(5,1), sigmaV(5,2), sigmaV(5,3),sigmaV(5,4),
*     +                sigmaV(6,1), sigmaV(6,2), sigmaV(6,3),sigmaV(6,4),
*     +                sigmaV(7,1), sigmaV(7,2), sigmaV(7,3),sigmaV(7,4),
*     +                sigmaV(8,1), sigmaV(8,2), sigmaV(8,3),sigmaV(8,4),
*     +                sigmaV(9,1), sigmaV(9,2), sigmaV(9,3),sigmaV(9,4)
* 3002        format(37(2x,1pe13.6))
      enddo
      close(unit=11)
      stop
      end
