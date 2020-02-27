.data 
X: .word 1,2,3,4,5
N: .word 5
SUM: .word 0


.text 
la R1,N
lwz R2,0(R1)
la R3,X
la R10,SUM

loop:
lwz R5,0(R3)
addi R3,R3,4
add  R4,R4,R5
addi R2,R2,-1
cmp 7,1,R2,R20
bc 1,28,loop 

stw R4,0(R10) 





