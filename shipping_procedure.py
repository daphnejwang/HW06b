#!/usr/bin/env python
import robots
import sys

class Cucurbits(object):

    def __init__(self, melon_type):
        self.melon_type = melon_type
        self.weight = 0.0
        self.color = None
        self.stickers = []

    def prep(self):
        # if self.melon_type is "Winter Squash":
        #     robots.painterbot.paint("Winter Squash")
        robots.cleanerbot.clean(self)
        robots.stickerbot.apply_logo(self)

    
    def __str__(self):
        if self.weight <= 0:
            return self.melon_type
        else:
            return "%s %0.2fLB %s" % (self.color, self.weight, self.melon_type)

class WinterSquash(Cucurbits):

    def prep(self):
        robots.painterbot.paint(self)
        robots.cleanerbot.clean(self)
        robots.stickerbot.apply_logo(self)

def main():
    f = open("standing_orders2.log")


    for line in f:
        (melon_type, quantity) = line.rstrip().split(':')
        try:
            quantity = int(quantity)
        except:
            quantity = 0
        
        count = 0
        cucurbits = []
        while len(cucurbits) < quantity:
            if count > 200:
                print "\nALL MELONS AND SQUASHES HAVE BEEN PICKED"
                print "ORDERS FAILED TO BE FULFILLED!"
                #break will just exit the loop, but exit will take you out of the system
                sys.exit()

            if melon_type == "WinterSquash":
                c = WinterSquash()
            else:
                c = Cucurbits(melon_type)

            robots.pickerbot.pick(c)
            count += 1
            
            c.prep()

            # evaluate cucurbits
            presentable = robots.inspectorbot.evaluate(c)
            if presentable:
                cucurbits.append(c)
            # elif:
            else:
                robots.trashbot.trash(c)
                continue

        print "------"
        print "Robots Picked %d %s for order of %d" % (count, melon_type, quantity)

        # Pack the cucurbits for shipping
        boxes = robots.packerbot.pack(cucurbits)
        # Ship the boxes
        robots.shipperbot.ship(boxes)
        print "------\n"


if __name__ == "__main__":
    main()
