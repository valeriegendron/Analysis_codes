      program sfr_map
*****************
*Author : Christian Carles

*Last update : 1 june 2017

*this program calculates the time and position of every sfr event by finding particules who go from gas to star.

*It outputs sfr_profile.out, giving for each time step, at increasing radius, the total wihtin gas mass, star mass, sfr, and ssfr. 
*format is  t then dist, gasmass, sfmass, sfr ssfr.

*It also output sfr_map.out, giving the position, radial distance, time of even and star mass of each star formation event. Format is : (rs(i,l),l=1,3), dist, t, ms(i)

*This program is to be used with the following GCDP output ASCII files :
*tzstep.dat, gXXXXXX, sXXXXXX

*******************
*declare parameters      
      implicit double precision (a-h,m,o-z)
*this excluse i, j, k, l, n variables who should be reserved for
*integers
      integer, parameter :: nmax=1000000, nbin=40
      real, parameter :: rmax=20.
      

*declare variables types

      character(7) :: filename
      real :: dr,  t, x, y, z, m,  MO, MFe, MZ, MHe, told, dist
      real :: distsfr
      integer :: tmax, ng, ng_old, ns, id, indec, id_star

* Arrays containing all particles.

      real, dimension(nbin) :: gasmass, sfmass
      real, dimension(nmax) :: ms, mg,  mzO, MzZ, MzHe, MzFe
      real, dimension(nmax,3):: rs, rg
      integer, dimension(nmax) :: flagfdg, ids, idg, idg_old

* Open files.

      open(unit=4,file='sfr_map.out',status='unknown')
      open(unit=12,file='sfr_profile.out',status='unknown')
      open(unit=9,file='tzstep.dat',status='old')
      read(9,9000) dummy
 9000 format(a3)
      told=0.
*Read number of time steps , not counting first line
      tmax = 0
      DO i=1,1000
      READ(9,*,IOSTAT=ios) junk
      IF (ios /= 0) EXIT
      tmax = tmax + 1
      ENDDO
      REWIND(9)
      print *,tmax

*define de bins sie based on parameters

      dr=rmax/real(nbin)
      print*,'bin size is',dir,'with nbins=',nbin
*Skip first line
      read(9,9000) dummy
* Loop over different time dumps

      do k=1,tmax
* initialize values for the radial binning
           do i=1,nbin
                gasmass(i)=0.
                sfmass(i)=0.
           enddo

* If not first dump, save data.

           if(k.gt.1) then
                do i=1,ng
                     idg_old(i)=idg(i)
                enddo
                ng_old=ng
           endif

* Get dump number and time in file tzstep.dat

           read(9,*,end=98) num, t
           write(6,2300) num, t
 2300      format(5x,'Dump number = ',i6,5x,'Time = ',1pe13.6)

* Open star dump and read data.

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

           open(unit=1,file=filename,status='old')
           ns=0
           do i=1,nmax
                read(1,*,end=90) (rs(i,j),j=1,3), (dummy,j=1,4), ms(i), 
     +                           (dummy,j=1,11), ids(i)
                ns=ns+1
           enddo
   90      close(unit=1)

* Open gas dump and read data.

           filename(1:1)='g'
           open(unit=1,file=filename,status='old')
           ng=0
           do i=1,nmax
                read(1,*,end=91) x, y, z, (dummy,j=1,3), m, 
     +                           (dummy,j=1,2), MHe, (dummy,j=1,2),
     +                           MO, (dummy,j=1,3), MFe, MZ,
     +                           id, flagfdg(i)

* Treat feedback particles as star particles.

                if(flagfdg(i).eq.0) then
                     ng=ng+1
                     rg(ng,1)=x
                     rg(ng,2)=y
                     rg(ng,3)=z
                     mg(ng)=m
                     idg(ng)=id
                     MzHe(ng)=MHe
                     MzO(ng)=MO
                     MzFe(ng)=MFe
                     MzZ(ng)=MZ
                else
                     ns=ns+1
                     rs(ns,1)=x
                     rs(ns,2)=y
                     rs(ns,3)=z
                     ms(ns)=m
                     ids(ns)=id
                endif
           enddo
   91      close(unit=1)

* Positions in kpc, masses in solar masses.

           do i=1,ns
                rs(i,1)=100.*rs(i,1)
                rs(i,2)=100.*rs(i,2)
                rs(i,3)=100.*rs(i,3)
                ms(i)=1.e+12*ms(i)
           enddo
           do i=1,ng
                rg(i,1)=100.*rg(i,1)
                rg(i,3)=100.*rg(i,2)
                rg(i,3)=100.*rg(i,3)
                mg(i)=1.e+12*mg(i)
           enddo

* If first dump, go to next dump.
           if(k.gt.1) then
*********************
*assign a bin to particles. index starts at 1 to not screw things when
*doing python later.

           do i=1,ng
                dist=sqrt((rg(i,1)**2)+(rg(i,2)**2))
                indec=int(dist/dr)+1
                if (indec.lt.nbin)  gasmass(indec)=gasmass(indec)+mg(i)
           enddo
*********************
* Look for star particles that were gas particles in previous step.

           do i=1,ns
                id_star=ids(i)
                do j=1,ng_old
                     if(idg_old(j).eq.id_star) then
                          dist=sqrt(rs(i,1)**2+rs(i,2)**2)
                          indec=int(dist/dr)+1
                          sfmass(indec)=sfmass(indec)+ms(i)
                          write(4,3000) (rs(i,l),l=1,3), dist, t, ms(i)
 3000                     format(6(2x,1pe13.6))
                          go to 3
                     endif
                enddo
    3      enddo
           dt=1.e+09*(t-told)

           do i=1,nbin
                distsfr=dr*(real(i-1)+0.5)
                sfr=sfmass(i)/dt
                if (sfr.gt.0.0001) then 
                        ssfr=sfr/gasmass(i)
                else
                        ssfr=0.
                endif        
                write(12,6001) t, distsfr, dr, gasmass(i),
     +                         sfmass(i), 
     +                         sfr, ssfr, i
 6001           format(7(2x,1pe13.6),2x,i3)
           enddo

           told=t
           endif
      enddo

   98 close(unit=4)
      close(unit=9)
      close(unit=12)

      stop
      end
