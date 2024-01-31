.text
.globl main

main:
    li      $a0,   0xC01830F1
    li      $a1,   0xC01830F1    
    li      $v0,   0
    jal     mul32x                    # $a1 * $a0 => $a1$a0
    la      $a3,   msg3
    move    $a2,   $a1
    move    $v1,   $v0
    jal     disp_adc64             # a3 - address of msg $v1(进位), $a2$a0 - 64bit
    
    li      $a0,   0xC01830F1
    li      $a1,   0xC01830F1  
    li      $v0,   0
    jal     mul32                   #   $a1 * $a0 => $a1$a0
    la      $a3,   msg4
    move    $a2,   $a1
    move    $v1,   $v0
    jal     disp_adc64           # a3 - address of msg $v1(进位), $a2$a0 - 64bit
    
    li      $v0,    10               # 返回系统
    syscall
    
#   $a1 * $a0 => $a1$a0
mul32x:
    multu $a0,$a1  # 乘积放在CPU内部的Hi和Low两个寄存器中
    mfhi  $a1      # move high reg to $a1
    mflo  $a0      # move low reg to $a0
    jr    $ra
    
#   $a1 * $a0 => $a1$a0
mul32:
    # ...
    addi $sp, $sp, -16
    sw $ra, 0($sp)
    sw $a0, 4($sp)
    addi $s4, $zero, 32
    move $a0, $zero

    move $s2, $a0
    move $s0, $a0
    sw $a1, 8($sp)
    sw $a0, 12($sp)	#$a1$a0右移一位
loop:
    beq $s4, $zero, exit
    move $v0, $zero
    lw $a0, 4($sp)
    jal sll32
    sw $a0, 4($sp)	#更新$a0的值
    move $s5, $v0	#存v0的数值
    
    lw $a1, 8($sp)
    lw $a0, 12($sp)
    move $v0, $zero
    jal srl64
    sw $a1, 8($sp)
    sw $a0, 12($sp)
    
    beq $s5, $zero while
    move $a2, $s2
    move $a0, $s0
    lw $a3, 8($sp)
    lw $a1, 12($sp)
    move $v0, $zero
    move $v1, $zero
    jal adc64
    move $s2, $a2
    move $s0, $a0
while:
    addi $s4, $s4, -1
    j loop
exit:
    lw $ra, 0($sp)
    addi $sp, $sp, 8
    move $a1, $a2
    addi $v0, $t4, 1
    jr $ra           
    
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

#   $v0(移入位) + $a1$a0 一起右移=> $a1$a0 + $v0(移出位)
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
    #   $a0 + $v0(移入位) 左移1位=> $v0(移出位) + $a0    $v0为0或1
sll32:
    #...
    addi $t0, $zero, 1
    sll $t0, $t0, 31
    and $t0, $t0, $a0
    srl $t0, $t0, 31
    sll $a0, $a0, 1
    or $a0, $a0, $v0
    move $v0, $t0
    jr $ra

#  $a1$a0 + $v0(移入位) 左移1位=> $v0(移出位) + $a1$a0  $v0为0或1
sll64: 
    # ...
    addi $sp, $sp, -8
    sw $ra, 0($sp)
    jal sll32
    sw $a0, 4($sp)
    move $a0, $a1
    jal sll32
    move $a1, $a0
    lw $a0, 4($sp)
    lw $ra, 0($sp)
    addi $sp, $sp, 8
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
       .asciiz "1st srl32: " # 字符串定义，以"00"字符作为终止符结束
   msg2:
       .asciiz "2st srl64: " # 字符串定义，以"00"字符作为终止符结束
   msg3:
       .asciiz "1st mul32: " # 字符串定义，以"00"字符作为终止符结束
   msg4:
       .asciiz "2nd mul32: " # 字符串定义，以"00"字符作为终止符结束
   errormsg:
       .asciiz "out of range(1 to 20)\n" # 字符串定义，以"00"字符作为终止符结束
   nline:  
       .asciiz "\n"  
   space:  
       .asciiz " "  
