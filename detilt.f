* Copied from program counter2.f, written by Simon Richard.
*
*     2019
*
      program detilt
      implicit double precision (a-h,m,o-z)

      parameter (nm=1000000)
      parameter (xunit=100)     ! length unit in kpc.
      parameter (vunit=207.4)   ! velocity unit in km/s.
      parameter (tunit=0.471)   ! time unit in Gyr.
      parameter (munit=1.e+12)  ! mass unit in M_sun.

      double precision jjx, jjy, jjz	
      double precision Js, Jxs, Jys, Jzs
      character filename *7, filename2 *8

      data filename2 /'*******r'/
      
* For star.
      
      dimension xs(nm), ys(nm), zs(NM), vxs(NM), vys(NM), vzs(nm),
     +          ms(nm), ms0s(NM), zHes(NM), zCs(NM), zNs(nm),
     +          zOs(nm), zNes(NM), zMgs(NM), zSis(NM), zFes(nm),
     +          zZs(nm), zg_p(NM), ts(NM), id(NM), flagfd(nm), age(nm),
     +          rhop(nm), h(NM), rhosp(NM), up(NM), rp(NM), vph(nm),
     +          vr(nm), thetap(nm)
      integer flagfd

* For gas.
      
      dimension xg(nm), yg(nm), zg(nm), vxg(nm), vyg(nm), vzg(nm),
     +          mg(nm), rhog(nm), ung(nm), mHeg(nm), mCg(nm),
     +          mNg(nm), mOg(nm), mNeg(nm), mMgg(nm), mSig(nm),
     +          mFeg(nm), mZg(nm), idg(nm), flagfd_p(nm), hg(nm),
     +          mug(nm), ndens(nm), tempg(nm), rpg(nm), divv(nm),
     +          pp(nm), cs(nm), dt(nm),
     +          vis(nm), vphg(nm), vrg(nm), rp3d(nm), as_p(nm),
     +          vr3d(nm), peffp(nm), ts_p(nm), alpvir(nm), thetapg(nm),
     +          flagc(nm), nnb(nm)
      integer flagfd_p, flagc
      double precision ndens
      
* For DM.
      
      dimension xd(Nm), yd(Nm), zd(Nm), vxd(Nm), vyd(Nm), vzd(Nm),
     +          md(Nm), pn(nm), dc(nm), vphd(nm), vrd(nm), rpd(nm),
     +          rhod(nm), hd(nm)
      integer pn

      write(6,1500)
 1500 format(/5x,'Enter dump number : ',$)
      read(5,*) ndump
      write(filename,1501) ndump
      if(ndump.lt.100000) write(filename,1502) ndump
      if(ndump.lt.10000) write(filename,1503) ndump
      if(ndump.lt.1000) write(filename,1504) ndump
      if(ndump.lt.100) write(filename,1505) ndump
      if(ndump.lt.10) write(filename,1506) ndump
 1501 format('s',i6)
 1502 format('s0',i5)
 1503 format('s00',i4)
 1504 format('s000',i3)
 1505 format('s0000',i2)
 1506 format('s00000',i1)
      open(unit=1,file=filename,status='old')
      filename2(1:7)=filename
      open(unit=11,file=filename2,status='unknown')

      filename(1:1)='g'
      open(unit=2,file=filename,status='old')
      filename2(1:7)=filename
      open(unit=12,file=filename2,status='unknown')

      filename(1:1)='d'
      open(unit=3,file=filename,status='old')
      filename2(1:7)=filename
      open(unit=13,file=filename2,status='unknown')

* Read data for stars.

      mstot=0.
      ns=0
      do i=1,nm
           read(1,153,end=80) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                        vzs(i), ms(i), ms0s(i), zHes(i), zCs(i),
     +                        zNs(i), zOs(i), zNes(i), zMgs(i),
     +                        zSis(i), zFes(i), zZs(i), zg_p(i), ts(i),
     +                        id(i), flagfd(i), age(i), rhop(i), h(i),
     +                        rhosp(i), up(i), rp(i), vph(i),
     +                        vr(i), thetap(i)
  153      format(19(1pe13.5),2(i10),9(1pe13.5))
           xs(i)=xs(i)*xunit
           ys(i)=ys(i)*xunit
           zs(i)=zs(i)*xunit
           vxs(i)=vxs(i)*vunit
           vys(i)=vys(i)*vunit
           vzs(i)=vzs(i)*vunit
           ts(i)=ts(i)*tunit
           ms(i)=ms(i)*munit
           mstot=mstot+ms(i)
           ns=ns+1
      enddo
   80 close(unit=1)
 		 		
* Read data for gas.

      mgtot=0.
      ng=0
      do i=1,nm
           read(2,101,end=21) xg(i), yg(i), zg(i), vxg(i), vyg(i),
     +                        vzg(i), mg(i), rhog(i), ung(i),
     +                        mHeg(i), mCg(i), mNg(i), mOg(i),
     +                        mNeg(i), mMgg(i), mSig(i), mFeg(i),
     +                        mZg(i), idg(i), flagfd_p(i), hg(i),
     +                        mug(i), ndens(i), tempg(i), rpg(i),
     +                        divv(i), pp(i),
     +                        cs(i), dt(i), vis(i), vphg(i), vrg(i),
     +                        rp3d(i), as_p(i), vr3d(i), peffp(i),
     +                        ts_p(i), alpvir(i), thetapg(i),
     +                        flagc(i), nnb(i)
  101      format(18(1pe13.5),2(i10),19(1pe13.5),2(i10))
           xg(i)=xg(i)*xunit
           yg(i)=yg(i)*xunit
           zg(i)=zg(i)*xunit
           vxg(i)=vxg(i)*vunit
           vyg(i)=vyg(i)*vunit
           vzg(i)=vzg(i)*vunit
           mg(i)=mg(i)*munit
           mgtot=mgtot+mg(i)
           ng=ng+1
      enddo
   21 close(unit=2)
      
* Read data for DM.

      mdtot=0.
      ndm=0
      do i=1,nm
           read(3,155,end=81) xd(i), yd(i), zd(i), vxd(i), vyd(i),
     +                        vzd(i), md(i), pn(nm), dc(i), vphd(i),
     +                        vrd(i), rpd(i), rhod(i), hd(i)
  155      format(7(1pe13.5),i10,6(1pe13.5))
           xd(i)=xd(i)*xunit
           yd(i)=yd(i)*xunit
           zd(i)=zd(i)*xunit
           vxd(i)=vxd(i)*vunit
           vyd(i)=vyd(i)*vunit
           vzd(i)=vzd(i)*vunit
           md(i)=md(i)*munit
           mdtot=mdtot+md(i)
           ndm=ndm+1
      enddo
   81 close(unit=3)

      write(6,1000) ndm, ng, ns
 1000 format(/5x,'Number of dark matter particles : ',i6
     +       /5X,'Number of gas particles         : ',i6
     +       /5X,'Number of star particles        : ',i6)

      write(6,1010) mdtot, mgtot, mstot
 1010 format(/5x,'Total mass of dark matter : ',1pe13.6
     +       /5X,'Total mass of gas         : ',1pe13.6
     +       /5X,'Total mass of stars       : ',1pe13.6)

* Calculate center of mass of stars.
      
      xcm=0.0
      ycm=0.0
      zcm=0.0
      vxcm=0.0
      vycm=0.0
      vzcm=0.0
      do i=1,ns
           xcm=xcm+xs(i)*ms(i)
           ycm=ycm+ys(i)*ms(i)
           zcm=zcm+zs(i)*ms(i)
           vxcm=vxcm+vxs(i)*ms(i)
           vycm=vycm+vys(i)*ms(i)
           vzcm=vzcm+vzs(i)*ms(i)
      enddo
      xcm=xcm/mstot
      ycm=ycm/mstot
      zcm=zcm/mstot
      vxcm=vxcm/mstot
      vycm=vycm/mstot
      vzcm=vzcm/mstot

      write(6,1300) xcm, ycm, zcm
 1300 format(/5x,'Center of mass of stars : ',3(2x,1pe13.6))

* Shift origin to center of mass.

      do i=1,ns
           xs(i)=xs(i)-xcm
           ys(i)=ys(i)-ycm
           zs(i)=zs(i)-zcm
           vxs(i)=vxs(i)-vxcm
           vys(i)=vys(i)-vycm
           vzs(i)=vzs(i)-vzcm
      enddo

      do i=1,ng
           xg(i)=xg(i)-xcm
           yg(i)=yg(i)-ycm
           zg(i)=zg(i)-zcm
           vxg(i)=vxg(i)-vxcm
           vyg(i)=vyg(i)-vycm
           vzg(i)=vzg(i)-vzcm
      enddo

      do i=1,ndm
           xd(i)=xd(i)-xcm
           yd(i)=yd(i)-ycm
           zd(i)=zd(i)-zcm
           vxd(i)=vxd(i)-vxcm
           vyd(i)=vyd(i)-vycm
           vzd(i)=vzd(i)-vzcm
      enddo	

* Calculate angular momentum of stars.

      Jxs=0.
      Jys=0.
      Jzs=0.
      Js=0.
        
      do i=1,ns 
           Jxs=Jxs+ms(i)*(ys(i)*vzs(i)-zs(i)*vys(i))
           Jys=Jys+ms(i)*(zs(i)*vxs(i)-xs(i)*vzs(i))
           Jzs=Jzs+ms(i)*(xs(i)*vys(i)-ys(i)*vxs(i))
      enddo
      Js=sqrt(Jxs*Jxs+Jys*Jys+Jzs*Jzs)

      if(Js.gt.0.) then
           jjx=Jxs/Js
           jjy=Jys/Js
           jjz=Jzs/Js
           costh=jjz
           sinth=sqrt(1.-jjz*jjz)
           if(sinth.gt.0.) then
                sinph=jjy/sinth
                cosph=jjx/sinth
           endif
      else 
           cosph=1.
           sinph=0.
      endif
        
      ax=costh*cosph
      bx=costh*sinph
      cx=-sinth
      ay=-sinph
      by=cosph
      cy=0.
      az=sinth*cosph
      bz=sinth*sinph
      cz=costh

      amx=ax*jjx+bx*jjy+cx*jjz
      amy=ay*jjx+by*jjy+cy*jjz
      amz=az*jjx+bz*jjy+cz*jjz

      write(6,2000) jjx, jjy, jjz
 2000 format(/5x,'Normalized angular momentum : ',3(2x,f10.8))
      write(6,2001) amx, amy, amz
 2001 format(/5x,'After rotation :              ',3(2x,f10.8))

* Rotate positions and velocities.

      do i=1,ns
           tx=xs(i)
           ty=ys(i)
           tz=zs(i)
           xs(i)=ax*tx+bx*ty+cx*tz
           ys(i)=ay*tx+by*ty+cy*tz
           zs(i)=az*tx+bz*ty+cz*tz

           tx=vxs(i)
           ty=vys(i)
           tz=vzs(i)
           vxs(i)=ax*tx+bx*ty+cx*tz
           vys(i)=ay*tx+by*ty+cy*tz
           vzs(i)=az*tx+bz*ty+cz*tz
      enddo

      do i=1,ng
           tx=xg(i)
           ty=yg(i)
           tz=zg(i)
           xg(i)=ax*tx+bx*ty+cx*tz
           yg(i)=ay*tx+by*ty+cy*tz
           zg(i)=az*tx+bz*ty+cz*tz
      
           tx=vxg(i)
           ty=vyg(i)
           tz=vzg(i)
           vxg(i)=ax*tx+bx*ty+cx*tz
           vyg(i)=ay*tx+by*ty+cy*tz
           vzg(i)=az*tx+bz*ty+cz*tz
      enddo

      do i=1,ndm
           tx=xd(i)
           ty=yd(i)
           tz=zd(i)
           xd(i)=ax*tx+bx*ty+cx*tz
           yd(i)=ay*tx+by*ty+cy*tz
           zd(i)=az*tx+bz*ty+cz*tz
      
           tx=vxd(i)
           ty=vyd(i)
           tz=vzd(i)
           vxd(i)=ax*tx+bx*ty+cx*tz
           vyd(i)=ay*tx+by*ty+cy*tz
           vzd(i)=az*tx+bz*ty+cz*tz
      enddo

* Print files.
      
      do i=1,ns
           write(11,153) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                   vzs(i), ms(i), ms0s(i), zHes(i), zCs(i),
     +                   zNs(i), zOs(i), zNes(i), zMgs(i),
     +                   zSis(i), zFes(i), zZs(i), zg_p(i), ts(i),
     +                   id(i), flagfd(i), age(i), rhop(i), h(i),
     +                   rhosp(i), up(i), rp(i), vph(i),
     +                   vr(i), thetap(i)
      enddo
			   
      do i=1,ng
           write(12,101) xg(i), yg(i), zg(i), vxg(i), vyg(i),
     +                   vzg(i), mg(i), rhog(i), ung(i),
     +                   mHeg(i), mCg(i), mNg(i), mOg(i),
     +                   mNeg(i), mMgg(i), mSig(i), mFeg(i),
     +                   mZg(i), idg(i), flagfd_p(i), hg(i),
     +                   mug(i), ndens(i), tempg(i), rpg(i),
     +                   divv(i), pp(i),
     +                   cs(i), dt(i), vis(i), vphg(i), vrg(i),
     +                   rp3d(i), as_p(i), vr3d(i), peffp(i),
     +                   ts_p(i), alpvir(i), thetapg(i),
     +                   flagc(i), nnb(i)
      enddo

      do i=1,ndm
           write(13,155) xd(i), yd(i), zd(i), vxd(i), vyd(i),
     +                   vzd(i), md(i), pn(nm), dc(i), vphd(i),
     +                   vrd(i), rpd(i), rhod(i), hd(i)
      enddo

      close(unit=11)
      close(unit=12)
      close(unit=13)

      stop
      end
