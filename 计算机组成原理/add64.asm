.text
.globl main

main:
    li      $a0,   0xC01830F1
    li      $a1,   0x205A0F26
    li      $a2,   0x7E341E86
    li      $a3,   0xA240F834
    li      $v1,   0
    jal     adc64                        #  $v1(进位) + $a3$a1 + $a2$a0 = $v1(进位) + $a2$a0 
    
    la      $a3,    msg1
    jal     disp_adc64               # a3 - address of msg $v1(进位), $a2$a0 - 64bit
    
    li      $a0,   0x7E341E86
    li      $a1,   0xA240F834
    li      $a2,   0xC01830F1
    li      $a3,   0x205A0F26
    li      $v1,   1
    jal     adc64                       #  $v1(进位) + $a3$a1 + $a2$a0 = $v1(进位) + $a2$a0 
    
    la      $a3,    msg2
    jal     disp_adc64               # a3 - address of msg $v1(进位), $a2$a0 - 64bit
        
    li      $v0,    10                  # 返回系统
    syscall
    
#  $v1(进位) + $a3$a1 + $a2$a0 = $v1(进位) + $a2$a0 
adc64:
   #...
   addi $sp, $sp, -8
   sw $ra, 0($sp)
   jal adc32
   sw $v0, 4($sp)
   move $a1, $a3
   move $a0, $a2
   jal adc32 
   move $a2, $v0
   lw $a0, 4($sp)
   
   lw $ra, 0($sp)
   addi $sp, $sp, 8
   jr   $ra    
   

#  $v1(进位) + $a1 + $a0 = $v1(进位) + $v0 
adc32: 
    #...
    addu $v0, $a0, $a1
    sltu $t3, $v0, $a0
    sltu $t4, $v0, $a1
    addu $v0, $v0, $v1
    addi $t2, $zero, 2
    add $t3, $t3, $t4
    beq $t3, $t2 set
    j set_exit
set:
    addi $v1, $zero, 1
    j return
set_exit:
    addi $v1, $zero, 0
return:
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
