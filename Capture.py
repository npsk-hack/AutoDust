import cv2
import subprocess, os

def CaptureProcess(objects):

    temp = []
    for i in objects:
        if i[0]=="person":
            objects.remove(i)
        else:
            temp.append(i[1])

    if len(temp)>0:
        m = max(temp)
        ind = temp.index(m)
        highest = objects[ind][0]
    else:
        highest=""
        
    #0-BIO - Key assocaition for Biodegradable Substances
    #1-NON-BIO - Key association for Non-Biodegradable Substances
    
    def dbcreation(): #creates object database
        x = {}
        for i in "bird.cat.dog.horse.sheep.cow.elephant.bear.zebra.giraffe.banana.apple.sandwich.orange.broccoli.carrot.hot dog.pizza.donut.cake.chair.sofa.pottedplant".split("."):
            x[i] = 0

        for i in "bench.parking meter.stop sign.fire hydrant.traffic light.boat.truck.train.bus.aeroplane.motorbike.car.bicycle.backpack.umbrella.handbag.tie.suitcase.frisbee.skis.snowboard.sports ball.kite.baseball bat.baseball glove.skateboard.surfboard.tennis racket.bottle.wine glass.cup.fork.knife.spoon.bowl.bed.diningtable.toilet.tvmonitor.laptop.mouse.remote.keyboard.cell phone.microwave.oven.toaster.sink.refrigerator.book.clock.vase.scissors.teddy bear.hair drier.toothbrush".split("."):
            x[i] = 1

        return x

    db = dbcreation() #creates the database object

    if highest!="":
        val = db[highest]
    else:
        val = " "

    return highest, val #returns found objects and their correlating key associations

