.text
.globl main

main:
    li      $a0,   0xC01830F0  
    li      $v0,   1
    jal     srl32              #   $v0(移入位) + $a0 一起右移1位=> $a0 + $v0(移出位)
    la      $a2,   msg1
    move    $a1,   $v0
    jal     disp_adc32         # $a2 - address of msg $a1- carry bit a0 - 32bits

    li      $a0,   0xC01830F1  
    li      $v0,   0
    jal     srl32              #   $v0(移入位) + $a0 一起右移1位=> $a0 + $v0(移出位)
    la      $a2,   msg2
    move    $a1,   $v0
    jal     disp_adc32         # $a2 - address of msg $a1- carry bit a0 - 32bits
     
    li      $v0,    10         # 返回系统
    syscall

#   $v0(移入位) + $a0 一起右移1位=> $a0 + $v0(移出位)
srl32: 
    #  ...
    andi $t0, $a0, 1
    add $t1, $zero, $v0
    sll $t1, $t1, 31
    srl $a0, $a0, 1
    or $a0, $t1, $a0
    move $v0, $t0
    jr $ra

# $a2 - address of msg $a1- carry bit a0 - 32bits
disp_adc32:
    move    $t0,  $a0
    move    $t1,  $a1
    move    $t2,  $a2
    
    li      $v0,   4                 # 打印字符串(功能号：4)
    move    $a0,   $t2               # 取字符串首地址
    syscall                          # 系统调用
    
    li      $v0,    1                # 打印十进制整数
    move    $a0,    $t1              # 输出进位位
    syscall                          # 系统调用
    
    li      $v0,    4                # 打印字符串(功能号：4)
    la      $a0,    space            # 输出空格" "          
    syscall
    
    li      $v0,    34               # 打印16进制整数，输出一整数
    move    $a0,    $t0              # 将输出的数据保存到$a0，为输出做准备
    syscall 
  
    li      $v0,    4                # 打印字符串(功能号：4)
    la      $a0,    nline            # 输出换行符，"\n"          
    syscall
    
    jr $ra
    
.data
   str1:
       .asciiz "please give an integer from 1 to 20: "
   msg1:
       .asciiz "1st srl32: "
   msg2:
       .asciiz "2st srl32: "
   errormsg:
       .asciiz "out of range(1 to 20)\n" # 字符串定义，以"00"字符作为终止符结束
   nline:  
       .asciiz "\n"  
   space:  
       .asciiz " "  
