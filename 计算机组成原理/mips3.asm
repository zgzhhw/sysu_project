.text
.globl main

main:
    la     $a0, list
    addiu  $a1, $a0, 56
    la     $a2, buffer
    move $a1, $zero
    addi $a3, $zero, 14
    jal    msort
    
    la     $a0, list
    addiu  $a1, $a0, 56
    jal    displist   

    li      $v0,    10               # 返回系统
    syscall
    
   # 显示存储器中地址从$a0到$a1的数据
displist: 

   move $t2, $a0
   move $t1, $zero
loop:move $t4, $t1
   mul $t4, $t4, 4
   add $t3, $t2, $t4
   lw $a0, 0($t3)
   li $v0, 1
   syscall
   la $a0, space_char
   li $v0, 4
   syscall
   addi $t1, $t1, 1
   bne $t3, $a1 loop
   jr $ra
   
# 把存储器中地址从$a0到$a1的数据排序, $a2为缓冲区起始地址
msort:				#$a1=start,$a3=end
    add $t1, $a1, $a3		#mid= t1
    sra $t1, $t1, 1		#mid/=2
    addi $sp, $sp, -16
    sw $a1, 0($sp)
    sw $t1, 4($sp)
    sw $a3, 8($sp)
    sw $ra, 12($sp)
    slt $t0, $a1, $a3 
    bne $t0, $zero mergesort
    jr $ra
mergesort:
    lw $a3, 8($sp)
    lw $t1, 4($sp)
    lw $a1, 0($sp)
    move $a3, $t1
    jal msort
    lw $a3, 8($sp)
    lw $t1, 4($sp)
    lw $a1, 0($sp)
#第二次调用
    addi $t2, $t1, 1
    move $a1, $t2
    jal msort
    lw $a3, 8($sp)
    lw $t1, 4($sp)
    lw $a1, 0($sp)
    jal merge
    lw $ra, 12($sp)
    addi $sp, $sp, 16
    jr $ra
    
merge:
    move $t0, $a1 		#t0=start
    move $t1, $a3		#t1=end
    slt $t2, $t0, $t1
    beq $t2, $zero exit
    add $t3, $t0, $t1
    sra $t3, $t3, 1		#t3=mid
    addi $t4, $t3, 1		#t4=mid+1
    move $t5, $t0		#t5=i=start
    move $t6, $t4		#t6=j=mid+1
    move $s0, $zero		#s0=k=0
loop1:
    slt $t7, $t3, $t5		#判断条件
    bne $t7, $zero, while_exit
    slt $t7, $t1, $t6
    bne $t7, $zero, while_exit
    
    sll $t8, $t5, 2		#offset=4
    sll $t9, $t6, 2
    sll $s1, $s0, 2
    add $t8, $t8, $a0		#offset+nums
    add $t9, $t9, $a0
    add $s1, $s1, $a2
    lw $s2, 0($t8)		#nums[i]
    lw $s3, 0($t9)		#nums[j]
    slt $t7, $s2, $s3		
    beq $t7, $zero getj
    sw $s2, 0($s1)
    addi $t5, $t5, 1
    addi $s0, $s0, 1
    j go
getj:
    sw $s3, 0($s1)
    addi $t6, $t6, 1
    addi $s0, $s0, 1
go:
    j loop1
while_exit:
loopi:
    slt $t7, $t3, $t5
    bne $t7, $zero, loopj
    sll $s1, $s0, 2
    add $s1, $a2, $s1		#获取k的位置
    sll $s2, $t5, 2
    add $s2, $a0, $s2		#获取i的位置
    lw $t7, 0($s2)
    sw $t7, 0($s1)
    addi $t5, $t5, 1
    addi $s0, $s0, 1
    j loopi
loopj:
    slt $t7, $t1, $t6
    bne $t7, $zero, while_jexit
    sll $s1, $s0, 2
    add $s1, $a2, $s1		#获取k的位置
    sll $s2, $t6, 2
    add $s2, $a0, $s2		#获取j的位置
    lw $t7, 0($s2)
    sw $t7, 0($s1)
    addi $t6, $t6, 1
    addi $s0, $s0, 1
    j loopj
while_jexit:
    move $t5, $t0		#i=start
    move $s0, $zero		#k=0
loop_load:
    slt $t7, $t1, $t5
    bne $t7, $zero, exit
    sll $s1, $t5, 2
    sll $s2, $s0, 2
    add $s1, $a0, $s1
    add $s2, $a2, $s2
    lw $s3, 0($s2)
    sw $s3, 0($s1)
    addi $t5, $t5, 1
    addi $s0, $s0, 1
    j loop_load
exit:
    jr $ra
.data
   list: 
       .word  30,213,951,583,674,13,97,345,980,786,108,12,833,965,528
   buffer:
       .space 256
   space_char:
       .asciiz " "
   
