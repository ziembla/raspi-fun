#!/usr/bin/python
# encoding: utf-8

from mcpi.minecraft import Minecraft
mc = Minecraft.create()

mc.postToChat("Hello!")

#pos = mc.player.getPos()
x, y, z = mc.player.getPos()

mc.player.setPos(x, y+10, z)

from mcpi import block

n = 5
l = [ block.WOOD, block.LEAVES, block.COBWEB ]
for q in range(len(l)):
	for i in range(n):
		for j in range(n):
			for k in range(n):
				mc.setBlock(5+x+1+i + q*n, y+j, z+k, l[q].id)

mc.setBlocks(x-n, y+12, z-n, x+n, y+12 +2*n, z+n, block.OBSIDIAN.id)

for i in range(100):
	mc.setBlock(x, y+1, 3+z+i, block.TNT.id, 1)

from time import sleep

mc.setBlock(x-10, y+3, z-10, block.LAVA.id)
sleep(20)
mc.setBlock(x-10, y+5, z-10, block.WATER.id)
sleep(10)
mc.setBlock(x-10, y+5, z-10, block.AIR.id)
mc.setBlock(x-10, y+3, z-10, block.AIR.id)

while True:
	p = mc.player.getTilePos()
	#b = mc.getBlock(p)
	#print(b)
	mc.setBlock(mc.player.getPos(), block.MUSHROOM_RED) #block.FLOWER_CYAN) #block.MUSHROOM_RED)
	sleep(0.5)
