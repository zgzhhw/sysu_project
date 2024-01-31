.text
.globl main
        # 把$a1指向的字符串拷贝到$a0指向的字符串
main:   la $a1, str1
        la $a0, str2
        li $a2, 110
        jal strcpy
        
        li  $v0, 4
        la  $a0, str2
        syscall
                
        li $v0, 10 		# 10 is the exit syscall.
        syscall 		# do the syscall

# strcpy_s(x,y,n)
# 功能： 把以0结尾的字符串y拷贝到字符串x中，拷贝的长度不能超过y的大小n
# 参数：addresses of x, y in $a0, $a1
#       n in $a2
strcpy:
    addi $sp, $sp, -4
    sw $s0, 0($sp)
    add $s0, $zero, $zero
L1: add $t1, $s0, $a1
    lbu $t2, 0($t1)
    add $t3, $s0, $a0
    sb  $t2, 0($t3)
    beq $t2, $zero, L2
    beq $s0, $a2, L2
    addi, $s0, $s0, 1
    j L1
    
L2: lw $s0, 0($sp)
    addi, $sp, $sp, 4
    jr   $ra               # and return
    
.data
str2:
   .space 200
str1:
   .asciiz "please give an integer from 1 to 20 "
  
  
