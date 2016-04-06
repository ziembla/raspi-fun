#!/usr/bin/python
# encoding: utf-8

from mcpi.minecraft import Minecraft
mc = Minecraft.create()

mc.postToChat("Hello! ąćę")

#pos = mc.player.getPos()
x, y, z = mc.player.getPos()

mc.player.setPos(x, y+20, z)

from mcpi import block

n = 5
l = [ block.CACTUS, block.SNOW, block.COBWEB ]
for q in range(len(l)):
	for i in range(n):
		for j in range(n):
			for k in range(n):
				mc.setBlock(100+x+1+i + q*len(l), y+j, z+k, l[q].id)

mc.setBlocks(200+x+1, y, z, x+10+n, y+n, z+n, block.OBSIDIAN.id)

for i in range(100):
	mc.setBlock(300+x+1, y+i, z+1, block.TNT.id, 1)
                 
from time import sleep

mc.setBlock(x+3, y+3, z, block.LAVA.id)
sleep(30)
mc.setBlock(x+3, y+5, z, block.WATER.id)
sleep(10)
mc.setBlock(x+3, y+5, z, block.AIR.id)
mc.setBlock(x+3, y+3, z, block.AIR.id)

while True:
	p = mc.player.getTilePos()
	#b = mc.getBlock(p)
	#print(b)
	mc.setBlock(mc.player.getPos(), block.MUSHROOM_RED) #block.FLOWER_CYAN) #block.MUSHROOM_RED)
	sleep(0.5)
