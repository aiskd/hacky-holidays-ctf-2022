# Crack The Password
* essentially following this: https://swanandx.github.io/blog/posts/re/ctfs/
* ran `$ strings CrackThePassword`
```
/lib64/ld-linux-x86-64.so.2
mgUa
puts
stdin
printf
fgets
strlen
__cxa_finalize
__libc_start_main
libc.so.6
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u+UH
[]A\A]A^A_
Please enter the password: 
Access granted!
Access denied!
;*3$"
GCC: (Debian 11.3.0-1) 11.3.0
Scrt1.o
__abi_tag
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
CrackThePassword.c
__FRAME_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
puts@GLIBC_2.2.5
stdin@GLIBC_2.2.5
_edata
strlen@GLIBC_2.2.5
printf@GLIBC_2.2.5
__libc_start_main@GLIBC_2.2.5
fgets@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
validatePassword
__libc_csu_init
__bss_start
main
__TMC_END__
_ITM_registerTMCloneTable
__cxa_finalize@GLIBC_2.2.5
.symtab
.strtab
.shstrtab
.interp
.note.gnu.property
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.got.plt
.data
.bss
.comment
```
* we run ``
* which produces
```
$ gdb -q CrackThePassword
Reading symbols from CrackThePassword...
(No debugging symbols found in CrackThePassword)
```
* then we set the dissasembly flavour using `set disassembly-flavor intel`
```
(gdb) set disassembly-flavor intel
```
* and look at the functions using `info functions`
```shell
(gdb) info functions
All defined functions:

Non-debugging symbols:
0x0000000000001000  _init
0x0000000000001030  puts@plt
0x0000000000001040  strlen@plt
0x0000000000001050  printf@plt
0x0000000000001060  fgets@plt
0x0000000000001070  __cxa_finalize@plt
0x0000000000001080  _start
0x00000000000010b0  deregister_tm_clones
0x00000000000010e0  register_tm_clones
0x0000000000001120  __do_global_dtors_aux
0x0000000000001160  frame_dummy
0x0000000000001169  validatePassword
0x0000000000001607  main
0x0000000000001680  __libc_csu_init
0x00000000000016e0  __libc_csu_fini
0x00000000000016e4  _fini
```
* let's disassemble main using `disassemble main`
```shell
(gdb) disassemble main
Dump of assembler code for function main:
   0x0000000000001607 <+0>:     push   rbp
   0x0000000000001608 <+1>:     mov    rbp,rsp
   0x000000000000160b <+4>:     sub    rsp,0x40
   0x000000000000160f <+8>:     mov    DWORD PTR [rbp-0x34],edi
   0x0000000000001612 <+11>:    mov    QWORD PTR [rbp-0x40],rsi
   0x0000000000001616 <+15>:    lea    rax,[rip+0x9e7]        # 0x2004
   0x000000000000161d <+22>:    mov    rdi,rax
   0x0000000000001620 <+25>:    mov    eax,0x0
   0x0000000000001625 <+30>:    call   0x1050 <printf@plt>
   0x000000000000162a <+35>:    mov    rdx,QWORD PTR [rip+0x2a1f]        # 0x4050 <stdin@GLIBC_2.2.5>
   0x0000000000001631 <+42>:    lea    rax,[rbp-0x30]
   0x0000000000001635 <+46>:    mov    esi,0x22
   0x000000000000163a <+51>:    mov    rdi,rax
   0x000000000000163d <+54>:    call   0x1060 <fgets@plt>
   0x0000000000001642 <+59>:    lea    rax,[rbp-0x30]
   0x0000000000001646 <+63>:    mov    rdi,rax
   0x0000000000001649 <+66>:    call   0x1169 <validatePassword>
   0x000000000000164e <+71>:    test   eax,eax
   0x0000000000001650 <+73>:    je     0x1663 <main+92>
   0x0000000000001652 <+75>:    lea    rax,[rip+0x9c7]        # 0x2020
   0x0000000000001659 <+82>:    mov    rdi,rax
   0x000000000000165c <+85>:    call   0x1030 <puts@plt>
   0x0000000000001661 <+90>:    jmp    0x1672 <main+107>
   0x0000000000001663 <+92>:    lea    rax,[rip+0x9c6]        # 0x2030
   0x000000000000166a <+99>:    mov    rdi,rax
   0x000000000000166d <+102>:   call   0x1030 <puts@plt>
   0x0000000000001672 <+107>:   mov    eax,0x0
   0x0000000000001677 <+112>:   leave  
   0x0000000000001678 <+113>:   ret    
End of assembler dump.
```

```shell
(gdb) disassemble validatePassword 
Dump of assembler code for function validatePassword:
   0x0000555555555169 <+0>:     push   rbp
   0x000055555555516a <+1>:     mov    rbp,rsp
   0x000055555555516d <+4>:     sub    rsp,0x10
   0x0000555555555171 <+8>:     mov    QWORD PTR [rbp-0x8],rdi
   0x0000555555555175 <+12>:    mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555179 <+16>:    mov    rdi,rax
   0x000055555555517c <+19>:    call   0x555555555040 <strlen@plt>
   0x0000555555555181 <+24>:    cmp    rax,0x21
   0x0000555555555185 <+28>:    jne    0x555555555600 <validatePassword+1175>
   0x000055555555518b <+34>:    mov    rax,QWORD PTR [rbp-0x8]
   0x000055555555518f <+38>:    movzx  eax,BYTE PTR [rax]
   0x0000555555555192 <+41>:    mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555196 <+45>:    add    rdx,0x6
   0x000055555555519a <+49>:    movzx  edx,BYTE PTR [rdx]
   0x000055555555519d <+52>:    add    edx,edx
   0x000055555555519f <+54>:    sub    edx,0x1d
   0x00005555555551a2 <+57>:    cmp    al,dl
   0x00005555555551a4 <+59>:    jne    0x555555555600 <validatePassword+1175>
   0x00005555555551aa <+65>:    mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555551ae <+69>:    add    rax,0x1
   0x00005555555551b2 <+73>:    movzx  eax,BYTE PTR [rax]
   0x00005555555551b5 <+76>:    mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555551b9 <+80>:    add    rdx,0x13
   0x00005555555551bd <+84>:    movzx  edx,BYTE PTR [rdx]
   0x00005555555551c0 <+87>:    add    edx,0x5
   0x00005555555551c3 <+90>:    cmp    al,dl
   0x00005555555551c5 <+92>:    jne    0x555555555600 <validatePassword+1175>
   0x00005555555551cb <+98>:    mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555551cf <+102>:   add    rax,0x2
   0x00005555555551d3 <+106>:   movzx  eax,BYTE PTR [rax]
   0x00005555555551d6 <+109>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555551da <+113>:   add    rdx,0x8
   0x00005555555551de <+117>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555551e1 <+120>:   sar    dl,1
   0x00005555555551e3 <+122>:   add    edx,0x13
   0x00005555555551e6 <+125>:   cmp    al,dl
   0x00005555555551e8 <+127>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555551ee <+133>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555551f2 <+137>:   add    rax,0x3
   0x00005555555551f6 <+141>:   movzx  eax,BYTE PTR [rax]
   0x00005555555551f9 <+144>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555551fd <+148>:   add    rdx,0xf
   0x0000555555555201 <+152>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555204 <+155>:   add    edx,0x35
   0x0000555555555207 <+158>:   cmp    al,dl
   0x0000555555555209 <+160>:   jne    0x555555555600 <validatePassword+1175>
   0x000055555555520f <+166>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555213 <+170>:   add    rax,0x4
   0x0000555555555217 <+174>:   movzx  eax,BYTE PTR [rax]
   0x000055555555521a <+177>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x000055555555521e <+181>:   add    rdx,0x3
   0x0000555555555222 <+185>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555225 <+188>:   sub    edx,0x44
   0x0000555555555228 <+191>:   cmp    al,dl
   0x000055555555522a <+193>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555230 <+199>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555234 <+203>:   add    rax,0x5
   0x0000555555555238 <+207>:   movzx  eax,BYTE PTR [rax]
   0x000055555555523b <+210>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x000055555555523f <+214>:   add    rdx,0x11
   0x0000555555555243 <+218>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555246 <+221>:   add    edx,0x28
   0x0000555555555249 <+224>:   cmp    al,dl
   0x000055555555524b <+226>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555251 <+232>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555255 <+236>:   add    rax,0x6
   0x0000555555555259 <+240>:   movzx  eax,BYTE PTR [rax]
   0x000055555555525c <+243>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555260 <+247>:   add    rdx,0x16
   0x0000555555555264 <+251>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555267 <+254>:   sar    dl,1
   0x0000555555555269 <+256>:   cmp    al,dl
   0x000055555555526b <+258>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555271 <+264>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555275 <+268>:   add    rax,0x7
   0x0000555555555279 <+272>:   movzx  eax,BYTE PTR [rax]
   0x000055555555527c <+275>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555280 <+279>:   add    rdx,0x15
   0x0000555555555284 <+283>:   movzx  ecx,BYTE PTR [rdx]
   0x0000555555555287 <+286>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x000055555555528b <+290>:   add    rdx,0xb
   0x000055555555528f <+294>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555292 <+297>:   xor    edx,ecx
   0x0000555555555294 <+299>:   cmp    al,dl
   0x0000555555555296 <+301>:   jne    0x555555555600 <validatePassword+1175>
   0x000055555555529c <+307>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555552a0 <+311>:   add    rax,0x8
   0x00005555555552a4 <+315>:   movzx  eax,BYTE PTR [rax]
   0x00005555555552a7 <+318>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555552ab <+322>:   add    rdx,0x5
   0x00005555555552af <+326>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555552b2 <+329>:   xor    edx,0x7
   0x00005555555552b5 <+332>:   cmp    al,dl
   0x00005555555552b7 <+334>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555552bd <+340>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555552c1 <+344>:   add    rax,0x9
   0x00005555555552c5 <+348>:   movzx  eax,BYTE PTR [rax]
   0x00005555555552c8 <+351>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555552cc <+355>:   add    rdx,0xe
   0x00005555555552d0 <+359>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555552d3 <+362>:   sub    edx,0x21
   0x00005555555552d6 <+365>:   cmp    al,dl
   0x00005555555552d8 <+367>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555552de <+373>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555552e2 <+377>:   add    rax,0xa
   0x00005555555552e6 <+381>:   movzx  eax,BYTE PTR [rax]
   0x00005555555552e9 <+384>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555552ed <+388>:   add    rdx,0x1e
   0x00005555555552f1 <+392>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555552f4 <+395>:   add    edx,0x7
   0x00005555555552f7 <+398>:   cmp    al,dl
   0x00005555555552f9 <+400>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555552ff <+406>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555303 <+410>:   add    rax,0xb
   0x0000555555555307 <+414>:   movzx  eax,BYTE PTR [rax]
   0x000055555555530a <+417>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x000055555555530e <+421>:   add    rdx,0x10
   0x0000555555555312 <+425>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555315 <+428>:   add    edx,edx
   0x0000555555555317 <+430>:   cmp    al,dl
   0x0000555555555319 <+432>:   jne    0x555555555600 <validatePassword+1175>
   0x000055555555531f <+438>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555323 <+442>:   add    rax,0xc
   0x0000555555555327 <+446>:   movzx  eax,BYTE PTR [rax]
   0x000055555555532a <+449>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x000055555555532e <+453>:   add    rdx,0x9
   0x0000555555555332 <+457>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555335 <+460>:   mov    ecx,edx
   0x0000555555555337 <+462>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x000055555555533b <+466>:   add    rdx,0x1d
   0x000055555555533f <+470>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555342 <+473>:   add    edx,ecx
   0x0000555555555344 <+475>:   cmp    al,dl
   0x0000555555555346 <+477>:   jne    0x555555555600 <validatePassword+1175>
   0x000055555555534c <+483>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555350 <+487>:   add    rax,0xd
   0x0000555555555354 <+491>:   movzx  eax,BYTE PTR [rax]
   0x0000555555555357 <+494>:   cmp    al,0x31
   0x0000555555555359 <+496>:   jne    0x555555555600 <validatePassword+1175>
   0x000055555555535f <+502>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555363 <+506>:   add    rax,0xe
   0x0000555555555367 <+510>:   movzx  eax,BYTE PTR [rax]
   0x000055555555536a <+513>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x000055555555536e <+517>:   add    rdx,0x1d
   0x0000555555555372 <+521>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555375 <+524>:   add    edx,edx
   0x0000555555555377 <+526>:   add    edx,0x3
   0x000055555555537a <+529>:   cmp    al,dl
   0x000055555555537c <+531>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555382 <+537>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555386 <+541>:   add    rax,0xf
   0x000055555555538a <+545>:   movzx  edx,BYTE PTR [rax]
   0x000055555555538d <+548>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555391 <+552>:   movzx  eax,BYTE PTR [rax]
   0x0000555555555394 <+555>:   xor    eax,0x5
   0x0000555555555397 <+558>:   cmp    dl,al
   0x0000555555555399 <+560>:   jne    0x555555555600 <validatePassword+1175>
   0x000055555555539f <+566>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555553a3 <+570>:   add    rax,0x10
   0x00005555555553a7 <+574>:   movzx  eax,BYTE PTR [rax]
   0x00005555555553aa <+577>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555553ae <+581>:   add    rdx,0x12
   0x00005555555553b2 <+585>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555553b5 <+588>:   sar    dl,1
   0x00005555555553b7 <+590>:   movsx  edx,dl
   0x00005555555553ba <+593>:   add    edx,edx
   0x00005555555553bc <+595>:   cmp    al,dl
   0x00005555555553be <+597>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555553c4 <+603>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555553c8 <+607>:   add    rax,0x11
   0x00005555555553cc <+611>:   movzx  eax,BYTE PTR [rax]
   0x00005555555553cf <+614>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555553d3 <+618>:   add    rdx,0x14
   0x00005555555553d7 <+622>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555553da <+625>:   xor    edx,0x40
   0x00005555555553dd <+628>:   cmp    al,dl
   0x00005555555553df <+630>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555553e5 <+636>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555553e9 <+640>:   add    rax,0x12
   0x00005555555553ed <+644>:   movzx  eax,BYTE PTR [rax]
   0x00005555555553f0 <+647>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555553f4 <+651>:   add    rdx,0x17
   0x00005555555553f8 <+655>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555553fb <+658>:   xor    edx,0xa
   0x00005555555553fe <+661>:   cmp    al,dl
   0x0000555555555400 <+663>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555406 <+669>:   mov    rax,QWORD PTR [rbp-0x8]
   0x000055555555540a <+673>:   add    rax,0x13
   0x000055555555540e <+677>:   movzx  eax,BYTE PTR [rax]
   0x0000555555555411 <+680>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555415 <+684>:   add    rdx,0x7
   0x0000555555555419 <+688>:   movzx  edx,BYTE PTR [rdx]
   0x000055555555541c <+691>:   sub    edx,0x2
   0x000055555555541f <+694>:   cmp    al,dl
   0x0000555555555421 <+696>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555427 <+702>:   mov    rax,QWORD PTR [rbp-0x8]
   0x000055555555542b <+706>:   add    rax,0x14
   0x000055555555542f <+710>:   movzx  eax,BYTE PTR [rax]
   0x0000555555555432 <+713>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555436 <+717>:   add    rdx,0x1c
   0x000055555555543a <+721>:   movzx  ecx,BYTE PTR [rdx]
   0x000055555555543d <+724>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555441 <+728>:   add    rdx,0xa
   0x0000555555555445 <+732>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555448 <+735>:   xor    edx,ecx
   0x000055555555544a <+737>:   cmp    al,dl
   0x000055555555544c <+739>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555452 <+745>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555456 <+749>:   add    rax,0x15
   0x000055555555545a <+753>:   movzx  eax,BYTE PTR [rax]
   0x000055555555545d <+756>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555461 <+760>:   add    rdx,0x19
   0x0000555555555465 <+764>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555468 <+767>:   sar    dl,1
   0x000055555555546a <+769>:   cmp    al,dl
   0x000055555555546c <+771>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555472 <+777>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555476 <+781>:   add    rax,0x16
   0x000055555555547a <+785>:   movzx  eax,BYTE PTR [rax]
   0x000055555555547d <+788>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555481 <+792>:   add    rdx,0x1f
   0x0000555555555485 <+796>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555488 <+799>:   or     edx,0x61
   0x000055555555548b <+802>:   sub    edx,0x2
   0x000055555555548e <+805>:   cmp    al,dl
   0x0000555555555490 <+807>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555496 <+813>:   mov    rax,QWORD PTR [rbp-0x8]
   0x000055555555549a <+817>:   add    rax,0x17
   0x000055555555549e <+821>:   movzx  eax,BYTE PTR [rax]
   0x00005555555554a1 <+824>:   cmp    al,0x39
   0x00005555555554a3 <+826>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555554a9 <+832>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555554ad <+836>:   add    rax,0x18
   0x00005555555554b1 <+840>:   movzx  eax,BYTE PTR [rax]
   0x00005555555554b4 <+843>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555554b8 <+847>:   add    rdx,0x12
   0x00005555555554bc <+851>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555554bf <+854>:   movsx  edx,dl
   0x00005555555554c2 <+857>:   add    edx,edx
   0x00005555555554c4 <+859>:   cmp    al,dl
   0x00005555555554c6 <+861>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555554cc <+867>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555554d0 <+871>:   add    rax,0x19
   0x00005555555554d4 <+875>:   movzx  eax,BYTE PTR [rax]
   0x00005555555554d7 <+878>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555554db <+882>:   add    rdx,0x1a
   0x00005555555554df <+886>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555554e2 <+889>:   mov    ecx,edx
   0x00005555555554e4 <+891>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555554e8 <+895>:   add    rdx,0x10
   0x00005555555554ec <+899>:   movzx  edx,BYTE PTR [rdx]
   0x00005555555554ef <+902>:   add    edx,ecx
   0x00005555555554f1 <+904>:   cmp    al,dl
   0x00005555555554f3 <+906>:   jne    0x555555555600 <validatePassword+1175>
   0x00005555555554f9 <+912>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555554fd <+916>:   add    rax,0x1a
   0x0000555555555501 <+920>:   movzx  edx,BYTE PTR [rax]
   0x0000555555555504 <+923>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555508 <+927>:   add    rax,0xb
   0x000055555555550c <+931>:   movzx  eax,BYTE PTR [rax]
   0x000055555555550f <+934>:   mov    ecx,eax
   0x0000555555555511 <+936>:   shr    cl,0x7
   0x0000555555555514 <+939>:   add    eax,ecx
   0x0000555555555516 <+941>:   sar    al,1
   0x0000555555555518 <+943>:   add    eax,0x7
   0x000055555555551b <+946>:   cmp    dl,al
   0x000055555555551d <+948>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555523 <+954>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555527 <+958>:   add    rax,0x1b
   0x000055555555552b <+962>:   movzx  eax,BYTE PTR [rax]
   0x000055555555552e <+965>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555532 <+969>:   add    rdx,0x4
   0x0000555555555536 <+973>:   movzx  edx,BYTE PTR [rdx]
   0x0000555555555539 <+976>:   add    edx,0x7b
   0x000055555555553c <+979>:   add    edx,edx
   0x000055555555553e <+981>:   cmp    al,dl
   0x0000555555555540 <+983>:   jne    0x555555555600 <validatePassword+1175>
   0x0000555555555546 <+989>:   mov    rax,QWORD PTR [rbp-0x8]
   0x000055555555554a <+993>:   add    rax,0x1c
   0x000055555555554e <+997>:   movzx  eax,BYTE PTR [rax]
   0x0000555555555551 <+1000>:  mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555555 <+1004>:  add    rdx,0x1
   0x0000555555555559 <+1008>:  movzx  edx,BYTE PTR [rdx]
   0x000055555555555c <+1011>:  sub    edx,0x13
   0x000055555555555f <+1014>:  cmp    al,dl
   0x0000555555555561 <+1016>:  jne    0x555555555600 <validatePassword+1175>
   0x0000555555555567 <+1022>:  mov    rax,QWORD PTR [rbp-0x8]
   0x000055555555556b <+1026>:  add    rax,0x1d
   0x000055555555556f <+1030>:  movzx  eax,BYTE PTR [rax]
   0x0000555555555572 <+1033>:  mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555576 <+1037>:  add    rdx,0x20
   0x000055555555557a <+1041>:  movzx  edx,BYTE PTR [rdx]
   0x000055555555557d <+1044>:  sub    edx,0x4d
   0x0000555555555580 <+1047>:  cmp    al,dl
   0x0000555555555582 <+1049>:  jne    0x555555555600 <validatePassword+1175>
   0x0000555555555584 <+1051>:  mov    rax,QWORD PTR [rbp-0x8]
   0x0000555555555588 <+1055>:  add    rax,0x1e
   0x000055555555558c <+1059>:  movzx  eax,BYTE PTR [rax]
   0x000055555555558f <+1062>:  mov    rdx,QWORD PTR [rbp-0x8]
   0x0000555555555593 <+1066>:  add    rdx,0x1f
   0x0000555555555597 <+1070>:  movzx  edx,BYTE PTR [rdx]
   0x000055555555559a <+1073>:  mov    ecx,edx
   0x000055555555559c <+1075>:  mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555555a0 <+1079>:  add    rdx,0x10
   0x00005555555555a4 <+1083>:  movzx  edx,BYTE PTR [rdx]
   0x00005555555555a7 <+1086>:  mov    esi,edx
   0x00005555555555a9 <+1088>:  sub    ecx,esi
   0x00005555555555ab <+1090>:  mov    edx,ecx
   0x00005555555555ad <+1092>:  cmp    al,dl
   0x00005555555555af <+1094>:  jne    0x555555555600 <validatePassword+1175>
   0x00005555555555b1 <+1096>:  mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555555b5 <+1100>:  add    rax,0x1f
   0x00005555555555b9 <+1104>:  movzx  eax,BYTE PTR [rax]
   0x00005555555555bc <+1107>:  mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555555c0 <+1111>:  add    rdx,0xd
   0x00005555555555c4 <+1115>:  movzx  edx,BYTE PTR [rdx]
   0x00005555555555c7 <+1118>:  add    edx,edx
   0x00005555555555c9 <+1120>:  add    edx,0x1
   0x00005555555555cc <+1123>:  cmp    al,dl
   0x00005555555555ce <+1125>:  jne    0x555555555600 <validatePassword+1175>
   0x00005555555555d0 <+1127>:  mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555555d4 <+1131>:  add    rax,0x20
   0x00005555555555d8 <+1135>:  movzx  eax,BYTE PTR [rax]
   0x00005555555555db <+1138>:  mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555555df <+1142>:  add    rdx,0xf
   0x00005555555555e3 <+1146>:  movzx  edx,BYTE PTR [rdx]
   0x00005555555555e6 <+1149>:  mov    ecx,edx
   0x00005555555555e8 <+1151>:  mov    rdx,QWORD PTR [rbp-0x8]
   0x00005555555555ec <+1155>:  add    rdx,0x4
   0x00005555555555f0 <+1159>:  movzx  edx,BYTE PTR [rdx]
   0x00005555555555f3 <+1162>:  add    edx,ecx
   0x00005555555555f5 <+1164>:  cmp    al,dl
   0x00005555555555f7 <+1166>:  jne    0x555555555600 <validatePassword+1175>
   0x00005555555555f9 <+1168>:  mov    eax,0x1
   0x00005555555555fe <+1173>:  jmp    0x555555555605 <validatePassword+1180>
   0x0000555555555600 <+1175>:  mov    eax,0x0
   0x0000555555555605 <+1180>:  leave  
   0x0000555555555606 <+1181>:  ret    
End of assembler dump.
```
Reading assembly: https://www.cs.virginia.edu/~evans/cs216/guides/x86.html

