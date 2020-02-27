      .data
msg:   .asciiz "Hello World"
       .text
main:
addi R0,R0,1      
la R3,msg    
syscall