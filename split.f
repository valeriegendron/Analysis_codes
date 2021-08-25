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
      character filename *7, filename2 *9

      data filename2 /'*******_*'/
      
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
     +     mNg(nm), mOg(nm), mNeg(nm), mMgg(nm), mSig(nm),
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
      filename2(9:9)='1'
      open(unit=11,file=filename2,status='unknown')
      filename2(9:9)='2'
      open(unit=12,file=filename2,status='unknown')

      filename(1:1)='g'
      open(unit=2,file=filename,status='old')
      filename2(1:7)=filename
      filename2(9:9)='1'
      open(unit=21,file=filename2,status='unknown')
      filename2(9:9)='2'
      open(unit=22,file=filename2,status='unknown')

      filename(1:1)='d'
      open(unit=3,file=filename,status='old')
      filename2(1:7)=filename
      filename2(9:9)='1'
      open(unit=31,file=filename2,status='unknown')
      filename2(9:9)='2'
      open(unit=32,file=filename2,status='unknown')

* Read data for stars.

      do i=1,nm
           read(1,153,end=80) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                        vzs(i), ms(i), ms0s(i), zHes(i), zCs(i),
     +                        zNs(i), zOs(i), zNes(i), zMgs(i),
     +                        zSis(i), zFes(i), zZs(i), zg_p(i), ts(i),
     +                        id(i), flagfd(i), age(i), rhop(i), h(i),
     +                        rhosp(i), up(i), rp(i), vph(i),
     +                        vr(i), thetap(i)
           if(id(i).lt.128000) then
                write(11,153) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                        vzs(i), ms(i), ms0s(i), zHes(i), zCs(i),
     +                        zNs(i), zOs(i), zNes(i), zMgs(i),
     +                        zSis(i), zFes(i), zZs(i), zg_p(i), ts(i),
     +                        id(i), flagfd(i), age(i), rhop(i), h(i),
     +                        rhosp(i), up(i), rp(i), vph(i),
     +                        vr(i), thetap(i)
           else
                write(12,153) xs(i), ys(i), zs(i), vxs(i), vys(i),
     +                        vzs(i), ms(i), ms0s(i), zHes(i), zCs(i),
     +                        zNs(i), zOs(i), zNes(i), zMgs(i),
     +                        zSis(i), zFes(i), zZs(i), zg_p(i), ts(i),
     +                        id(i), flagfd(i), age(i), rhop(i), h(i),
     +                        rhosp(i), up(i), rp(i), vph(i),
     +                        vr(i), thetap(i)
 153            format(19(1pe13.5),2(i10),9(1pe13.5))
           endif
      enddo
   80 close(unit=1)
      close(unit=11)
      close(unit=12)
      
* Read data for gas.

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
           if(idg(i).lt.128000) then
                write(21,101) xg(i), yg(i), zg(i), vxg(i), vyg(i),
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
            else
                write(22,101) xg(i), yg(i), zg(i), vxg(i), vyg(i),
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
           endif
  101      format(18(1pe13.5),2(i10),19(1pe13.5),2(i10))
      enddo
   21 close(unit=2)
      close(unit=21)
      close(unit=22)

* Read data for DM.

      do i=1,nm
           read(3,155,end=81) xd(i), yd(i), zd(i), vxd(i), vyd(i),
     +                        vzd(i), md(i), pn(i), dc(i), vphd(i),
     +                        vrd(i), rpd(i), rhod(i), hd(i)
           if(pn(i).lt.320000) then
                write(31,155) xd(i), yd(i), zd(i), vxd(i), vyd(i),
     +                        vzd(i), md(i), pn(i), dc(i), vphd(i),
     +                        vrd(i), rpd(i), rhod(i), hd(i)
           else
                write(32,155) xd(i), yd(i), zd(i), vxd(i), vyd(i),
     +                        vzd(i), md(i), pn(i), dc(i), vphd(i),
     +                        vrd(i), rpd(i), rhod(i), hd(i)
           endif
 155       format(7(1pe13.5),i10,6(1pe13.5))
      enddo
   81 close(unit=3)
      close(unit=31)
      close(unit=32)

      stop
      end
