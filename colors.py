import colour 

theme=["#f94144","#f3722c","#f8961e","#f9c74f","#90be6d","#43aa8b","#577590"]


#theme = ["#264653","#287271","#2a9d8f","#8ab17d","#e9c46a","#f4a261","#e76f51"]

#theme = ["#84e3c8","#a8e6cf","#dcedc1","#ffd3b6","#ffaaa5","#ff8b94","#ff7480"]
for c in theme:
    c100 = colour.Color(c)
    h,s,l = colour.Color(c).hsl
    #c80 = colour.Color(hsl = (h,s,l*1.2))
    #c60 = colour.Color(hsl = (h,s,l*1.4))
    #c40 = colour.Color(hsl = (h,s,l*0.4))
    c80 = colour.Color(hsl = (h,s*0.6,l))
    c60 = colour.Color(hsl = (h,s,l*0.6))
    c40 = colour.Color(hsl = (h,s,l*0.4))
    print(c100.hex_l, c80.hex_l, c60.hex_l, c40.hex_l)

# theme 1
#f94144 #d46668 #b70609 #7a0406
#f3722c #cb7e54 #a33f09 #6d2a06
#f8961e #cc924a #a25b05 #6c3d03
#f9c74f #d7b971 #be8806 #7f5b04
#90be6d #92ae7d #557c37 #395325
#43aa8b #589583 #286653 #1b4438
#577590 #627485 #344656 #232f3a
#themn 2
#264653 #2e5464 #356274 #0f1c21
#287271 #308988 #38a09e #102e2d
#2a9d8f #32bcac #48cebe #113f39
#8ab17d #acc8a3 #cedec8 #354b2d
#e9c46a #f2dba5 #faf3e0 #765911
#f4a261 #f8c8a1 #fdede1 #803d09
#e76f51 #ef9c88 #f6cabf #6e220f
# theme 2
#264653 #2a444e #2f424a #334045
#287271 #2f6b6a #376363 #3e5c5b
#2a9d8f #359186 #41867e #4c7a75
#8ab17d #8dac82 #8fa787 #92a18d
#e9c46a #dcbf77 #d0b983 #c3b490
#f4a261 #e5a470 #d7a57e #c8a78d
#e76f51 #d87860 #c9816f #ba8a7e¨

# theme 3
#84e3c8 #8dd9c4 #28af89 #1b755b
#a8e6cf #aee0cd #35b988 #247c5b
#dcedc1 #dbe9c5 #91c63c #618527
#ffd3b6 #f8d4bd #ff6a07 #af4500
#ffaaa5 #f6b2ae #fc0e00 #a80900
#ff8b94 #f3979e #ec0012 #9e000c
#ff7480 #f1828b #df0013 #94000d