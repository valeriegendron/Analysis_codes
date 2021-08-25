      program warp

      implicit double precision (a-h,m,o-z)
      parameter (pi=3.14159265259)
      parameter (nmax=1000000)
      character filename *17
      dimension x(nmax), y(nmax), z(nmax), m(nmax)
      dimension zmean(1000), zsigma(1000), mtot(1000), nb(1000)

      data zmean, zsigma, mtot /3000*0./
      data nb /1000*0/

      data zmax /2.5/     ! can be adjusted by the user.
      
      data nwedge /8/    ! can be adjusted by the user.
      
      write(6,1000)
 1000 format(/5x,'Enter filename : ',$)
      read(5,8000) filename
 8000 format(a8)
      open(unit=1,file=filename,status='old')
      filename(9:17)='_warp.out'
      open(unit=2,file=filename,status='unknown')

* Read input file.

      n=0
      do i=1,nmax
           read(1,*,end=99) x(i), y(i), z(i), vx, vy, vz, m(i)
           n=n+1
      enddo
   99 close(unit=1)

* Calculate zmean and zsigma.

      write(6,1001)
 1001 format(/5x,'Enter rmin and rmax : ',$)
      read(5,*) rmin, rmax
      rmin2=rmin**2
      rmax2=rmax**2
      da=2.*pi/nwedge
      
      do i=1,n
           r2=x(i)**2+y(i)**2
           if(r2.ge.rmin2.and.r2.lt.rmax2.and.dabs(z(i)).le.zmax) then
                angle=datan2(y(i),x(i))
                if(angle.lt.0.) angle=angle+2.*pi
                index=int(angle/da)+1
                zmean(index)=zmean(index)+m(i)*z(i)
                mtot(index)=mtot(index)+m(i)
                nb(index)=nb(index)+1
           endif
      enddo
      do index=1,nwedge
           zmean(index)=zmean(index)/mtot(index)
      enddo
      
      do i=1,n
           r2=x(i)**2+y(i)**2
           if(r2.ge.rmin2.and.r2.lt.rmax2) then
                angle=datan2(y(i),x(i))
                if(angle.lt.0.) angle=angle+2.*pi
                index=int(angle/da)+1
                zsigma(index)=zsigma(index)+m(i)*(z(i)-zmean(index))**2
           endif
      enddo
        
      do index=1,nwedge
           zsigma(index)=sqrt(zsigma(index)/mtot(index))
      enddo

* Print results.

      do index=1,nwedge
           angle=(float(index)-0.5)*da
           write(2,2000) angle, zmean(index), zsigma(index), nb(index)
 2000      format(3(2x,1pe13.6),2x,i6)
      enddo
      close(unit=2)
          
      stop
      end
      
