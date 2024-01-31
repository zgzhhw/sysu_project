.text
.globl main

main:
   
    li      $a0,   0xC01830F1
    li      $a1,   0x205A0F26
    li      $v1,   0
    jal     adc32             # $v1(进位) + $a1 + $a0 = $v1(进位) + $v0 
    
    la      $a1,    msg1
    move    $a0,    $v0    
    jal     disp_adc32      # a1 - address of msg v1- carry bit a0 - 32bits
    
    li      $a0,   0x7E341E86
    li      $a1,   0xA240F834
    li      $v1,   0
    jal     adc32             # $v1(进位) + $a1 + $a0 = $v1(进位) + $v0 
    
    la      $a1,    msg2    
    move    $a0,    $v0
    jal     disp_adc32      # a1 - address of msg v1- carry bit a0 - 32bits
        
    li      $v0,    10          # 返回系统
    syscall
    
# $v1(进位) + $a1 + $a0 = $v1(进位) + $v0 
adc32: 
    #...
    addu $v0, $a0, $a1
    sltu $t3, $v0, $a0
    sltu $t4, $v0, $a1
    addi $t2, $zero, 2
    add $t3, $t3, $t4
    beq $t3, $t2 set
    j set_exit
set:
    addi $v1, $zero, 1
    addi $v0, $v0, 1
    j return
set_exit:
    addi $v1, $zero, 0
return:
    move $a0, $v0
    jr $ra
 
 
# a1 - address of msg v1- carry bit a0 - 32bits
disp_adc32:
    move    $t0,  $a0
    move    $t1,  $v1
    move    $t2,  $a1
    
    li      $v0,   4                 # 打印字符串(功能号：4)
    move    $a0,   $t2               # 取字符串首地址
    syscall                          # 系统调用
    
    li      $v0,    1                # 打印十进制整数
    move    $a0,    $t1              # 打印$t1中的数
    syscall                          # 系统调用
    
    li      $v0,    4                # 打印字符串(功能号：4)
    la      $a0,    space            # 输出空格" "          
    syscall
    
    li      $v0,    34               # 打印16进制整数，输出一整数
    move    $a0,    $t0              # 打印$t0中的数
    syscall 
  
    li      $v0,    4                # 打印字符串(功能号：4)
    la      $a0,    nline            # 输出换行符，"\n"          
    syscall
    
    jr $ra
    
.data
   str1:
       .asciiz "please give an integer from 1 to 20: "
   msg1:
       .asciiz "1st sum: " # 字符串定义，以"00"字符作为终止符结束
   msg2:
       .asciiz "2nd sum: " # 字符串定义，以"00"字符作为终止符结束
   errormsg:
       .asciiz "out of range(1 to 20)\n" # 字符串定义，以"00"字符作为终止符结束
   nline:  
       .asciiz "\n"  
   space:  
       .asciiz " "  
