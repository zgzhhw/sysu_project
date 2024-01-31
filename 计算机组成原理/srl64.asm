.text
.globl main

main:
    li      $a0,   0xC01830F1
    li      $a1,   0xC01830F1    
    li      $v0,   0
    jal     srl64              #  $v0(移入位) + $a1$a0 一起右移1位 => $a1$a0 + $v0(移出位)
    la      $a3,   msg3
    move    $a2,   $a1
    move    $v1,   $v0
    jal     disp_adc64         # a3 - address of msg $v1(进位), $a2$a0 - 64bit
            
    li      $a0,   0xC01830F0
    li      $a1,   0xC01830F1    
    li      $v0,   1
    jal     srl64              #  $v0(移入位) + $a1$a0 一起右移1位 => $a1$a0 + $v0(移出位)
    la      $a3,   msg4
    move    $a2,   $a1
    move    $v1,   $v0
    jal     disp_adc64         # a3 - address of msg $v1(进位), $a2$a0 - 64bit
    
    li      $v0,    10         # 返回系统
    syscall

#  $v0(移入位) + $a1$a0 一起右移1位 => $a1$a0 + $v0(移出位)
srl64: 
   # ...
    addi $sp, $sp, -8
    sw $ra, 0($sp)
    sw $a0, 4($sp)
    move $a0, $a1
    jal srl32
    move $a1, $a0
    lw $a0, 4($sp)
    jal srl32
    lw $ra, 0($sp)
    addi $sp, $sp, 8
    jr $ra
 
#   $v0(移入位) + $a0 一起右移1位=> $a0 + $v0(移出位)
srl32: 
    #  ...
    addi $sp, $sp, -4
    andi $t0, $a0, 1
    sw $t0, 0($sp)
    sll $v0, $v0, 31
    srl $a0, $a0, 1
    or $a0, $a0, $v0
    lw $v0, 0($sp)
    addi $sp, $sp, 4
    jr $ra

# a3 - address of msg $v1(进位), $a2$a0 - 64bit
disp_adc64:
    move    $t0,  $a0
    
    li      $v0,   4                 # 打印字符串(功能号：4)
    move    $a0,   $a3               # 取字符串首地址
    syscall                          # 系统调用
    
    li      $v0,    1                # 打印十进制整数
    move    $a0,    $v1              # 输出进位位
    syscall                          # 系统调用
    
    li      $v0,    4                # 打印字符串(功能号：4)
    la      $a0,    space            # 输出空格" "          
    syscall
    
    li      $v0,    34               # 打印16进制整数，输出一整数
    move    $a0,    $a2              # 输出高4个字节
    syscall 

    li      $v0,    4                # 打印字符串(功能号：4)
    la      $a0,    space            # 输出空格" "          
    syscall
      
    li      $v0,    34               # 打印16进制整数，输出一整数
    move    $a0,    $t0              # 输出低4个字节
    syscall       
    
    li      $v0,    4                # 打印字符串(功能号：4)
    la      $a0,    nline            # 输出换行符，"\n"          
    syscall
    
    jr $ra
    
.data
   str1:
       .asciiz "please give an integer from 1 to 20: "
   msg3:
       .asciiz "1st srl64: " 
   msg4:
       .asciiz "2st srl64: " 
   errormsg:
       .asciiz "out of range(1 to 20)\n" # 字符串定义，以"00"字符作为终止符结束
   nline:  
       .asciiz "\n"  
   space:  
       .asciiz " "  
