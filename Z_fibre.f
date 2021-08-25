      program Z_fiber
*

*****************
*Author : Christian Carles

*Last update : 1 june 2017

** This program calculates the evolution of element abundances within a given radius.

*It outputs Z_f.out, giving for each time step, withtin the given radius :
*the number of s and g particules, for gaseous H, O and Fe : the total mass, the mass that moved in during last step, the mass that moved out in last step, the mass consumed by SF during step, the mass outputed by feedback during step, the total variation during step, the Fe/H and O/H, and total mass of stars.

*format : t, nsf, ngf, mzHgtot, mH_movein, mH_moveout, mH_SF, mH_SN, deltaH1, mzOgtot, mO_movein, mO_moveout, mO_SF, mO_SN, deltaO1, OH, mzFegtot, mFe_movein, mFe_moveout, mFe_SF, mFe_SN, deltaFe1, FeH, mg, mg_movein, mg_moveout, Mg_SF, mg SN, deltamg, msf

*This program is to be used with the following GCDP output ASCII files :
* tzstep.dat, gXXXXXX, sXXXXXX.

*play with rad to control the range : 1 for classic fibre, more for bigger. 
*******************



      implicit double precision (a-h,m,o-z)
      parameter (nmax=1000000)

      character filename *7, dummyc *3

* Solar abundances.

      parameter (XSH=0.706d0)
      parameter (XSHe=0.275d0)
      parameter (XSC=3.03d-3)
      parameter (XSN=1.11d-3)
      parameter (XSO=9.59d-3)
      parameter (XSNe=1.62d-3)
      parameter (XSMg=5.15d-4)
      parameter (XSSi=6.53d-4)
      parameter (XSFe=1.17d-3)
      parameter (XSZ=0.19d0)
      parameter (rad=1.0)
* Arrays containing all particles.

      dimension rs(nmax,3), ms(nmax), rg(nmax,3), mzHg(nmax), 
     +          mzOg(nmax), mzFeg(nmax), ids(nmax), idg(nmax),
     +          mg(nmax)
      integer flagfdg(nmax)

* Arrays containing particles in fiber region.

      dimension lists(nmax), listg(nmax), mzHgf(nmax), mzOgf(nmax),
     +          mzFegf(nmax), mgf(nmax)

* Arrays containing  particles in fiber region at previous step.

      dimension lists_old(nmax), listg_old(nmax), mgf_old(nmax),
     +          mzHgf_old(nmax), mzOgf_old(nmax), mzFegf_old(nmax)

* Open files.

      open(unit=4,file='Z_f.out',status='unknown')
      open(unit=9,file='tzstep.dat',status='old')
      read(9,9000) dummyc
 9000 format(a3)
* Loop over dumps.
*Read number of time steps , not counting first line
      tmax=1000
      step_sim = 0
      DO i=1,tmax
      READ(9,*,IOSTAT=ios) junk
      IF (ios /= 0) EXIT
      step_sim = step_sim + 1
      ENDDO
      REWIND(9)
*Skip first line
      read(9,9000) dummyc

      do k=1,step_sim

* If not first dump, save data.

           if(k.gt.1) then
                do i=1,ngf
                     listg_old(i)=listg(i)
                     mzHgf_old(i)=mzHgf(i)
                     mzOgf_old(i)=mzOgf(i)
                     mzFegf_old(i)=mzFegf(i)
                     mgf_old(i)=mgf(i)
                enddo
                do i=1,nsf
                     lists_old(i)=lists(i)
                enddo
                ngf_old=ngf
                mzHgtot_old=mzHgtot
                mzOgtot_old=mzOgtot
                mzFegtot_old=mzFegtot
                mgtot_old=mgtot
                nsf_old=nsf
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
     +                           (dummy,j=1,2), mzHe, (dummy,j=1,2),
     +                           mzO, (dummy,j=1,3), mzFe, mzZ, id, 
     +                           flagfdg(i)

* Treat feedback particles as star particles.

                if(flagfdg(i).eq.0) then
                     ng=ng+1
                     mg(ng)=m
                     rg(ng,1)=x
                     rg(ng,2)=y
                     rg(ng,3)=z
                     mzOg(ng)=mzO
                     mzFeg(ng)=mzFe
                     idg(ng)=id
                     mzHg(ng)=1.e+12*m-mzHe-mzZ
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
                rg(i,2)=100.*rg(i,2)
                rg(i,3)=100.*rg(i,3)
                mg(i)=1.e+12*mg(i)
           enddo

* Calculate center, using star particles.

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

* Identify particles in fiber.
*
* NSF, NGF : # of star and gas particles in fiber.
* Store ID in arrays LIST?, hydrogen mass in arrays MZH?F,
* oxygen mass in arrays MZO?F, Iron mass in arrays MZFe?g.
*
*    star particles.
*
           nsf=0
           msf=0.
           do i=1,ns
                dist=dsqrt((rs(i,1)-xcm)**2+(rs(i,2)-ycm)**2)
                if(dist.LT.rad) then
                     nsf=nsf+1
                     lists(nsf)=ids(i)
                     msf=msf+ms(i)
                endif
           enddo

*    gas particles.

           mzHgtot=0.
           mzOgtot=0.
           mzFegtot=0.
           mgtot=0.
           ngf=0
           do i=1,ng
                dist=dsqrt((rg(i,1)-xcm)**2+(rg(i,2)-ycm)**2)
                if(dist.LT.rad) then
                     ngf=ngf+1
                     listg(ngf)=idg(i)
                     mgf(ngf)=mg(i)
                     mzHgf(ngf)=mzHg(i)
                     mzOgf(ngf)=mzOg(i)
                     mzFegf(ngf)=mzFeg(i)
                     mgtot=mgtot+mg(i)
                     mzHgtot=mzHgtot+mzHg(i)
                     mzOgtot=mzOgtot+mzOg(i)
                     mzFegtot=mzFegtot+mzFeg(i)
                endif
           enddo

* If first dump, go to next dump.

           if(k.eq.1) go to 10

* Calculate hydrogen and oxygen mass added to fiber or removed from fiber.
*
* 1) Gas particles in fiber that were not in fiber in previous dump.

           mH_movein=0.
           mO_movein=0.
           mFe_movein=0.
           mg_movein=0.
           do i=1,ngf
                id=listg(i)
                do j=1,ngf_old
                     if(listg_old(j).eq.id) go to 1
                enddo
                do j=1,nsf_old
                     if(lists_old(j).eq.id) go to 1
                enddo
                mH_movein=mH_movein+mzHgf(i)
                mO_movein=mO_movein+mzOgf(i)
                mFe_movein=mFe_movein+mzFegf(i)
                mg_movein=mg_movein+mgf(i)
    1      enddo

* 2) Gas particles outside of fiber that were in fiber in previous dump.

           mH_moveout=0.
           mO_moveout=0.
           mFe_moveout=0.
           mg_moveout=0.
           do i=1,ngf_old
                id=listg_old(i)
                do j=1,ngf
                     if(listg(j).eq.id) go to 2
                enddo
                do j=1,nsf
                     if(lists(j).eq.id) go to 2
                enddo
                mH_moveout=mH_moveout-mzHgf_old(i)
                mO_moveout=mO_moveout-mzOgf_old(i)
                mFe_moveout=mFe_moveout-mzFegf_old(i)
                mg_moveout=mg_mouveout-mgf_old(i)
    2      enddo

* 3) Metals removed by SF. Look for star particles that were gas particles
*    in previous step (both in fiber).

           mH_SF=0.
           mO_SF=0.
           mFe_SF=0.
           mg_SFR=0.
           do i=1,nsf
                id=lists(i)
                do j=1,ngf_old
                     if(listg_old(j).eq.id) then
                          mH_SF=mH_SF-mzHgf_old(j)
                          mO_SF=mO_SF-mzOgf_old(j)
                          mFe_SF=mFe_SF-mzFegf_old(j)
                          mg_SF=mg_SFR-mgf_old(j)
                          go to 3
                     endif
                enddo
    3      enddo

* 4) Metals added by SN.

           deltaH1=mzHgtot-mzHgtot_old
           deltaH2=mH_movein+mH_moveout+mH_SF
           mH_SN=deltaH1-deltaH2
           deltaO1=mzOgtot-mzOgtot_old
           deltaO2=mO_movein+mO_moveout+mO_SF
           mO_SN=deltaO1-deltaO2
           deltaFe1=mzFegtot-mzFegtot_old
           deltaFe2=mFe_movein+mFe_moveout+mFe_SF
           mFe_SN=deltaFe1-deltaFe2
           deltag1=mgtot-mgtot_old
           deltag2=mg_movein+mg_moveout_mg_SF
           mg_SN=deltag1-deltag2
* Write data.

           OH=dlog10(mzOgtot/mzHgtot)-dlog10(XSO/XSH)
           FeH=dlog10(mzFegtot/mzHgtot)-dlog10(XSFe/XSH)
           write(4,3000) t, nsf, ngf, 
     +                   mzHgtot, mH_movein, mH_moveout, mH_SF,
     +                   mH_SN, deltaH1,
     +                   mzOgtot, mO_movein, mO_moveout, mO_SF, 
     +                   mO_SN, deltaO1, OH,
     +                   mzFegtot, mFe_movein, mFe_moveout, mFe_SF, 
     +                   mFe_SN, deltaFe1, FeH,
     +                   mgtot, mg_movein, mg_moveout, mg_SFR,
     +                   mg_SN, deltaf1, msf
 3000      format(2x,1pe13.6,2(2x,i6),27(2x,1pe13.6))

   10 enddo

   98 close(unit=4)
      close(unit=9)

      stop
      end
