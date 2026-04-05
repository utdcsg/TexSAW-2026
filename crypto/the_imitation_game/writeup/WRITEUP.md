# The Imitation Game Writeup
## Ciphertext

> twhsnz{tngqmqdhqqygxrloyehuvxtwwvxklkiiudpxqcvqhbmkepledu}
> 
> zpzc xlcq aq lorr, dlh aas zyqg n paldee rn mate mpgsxm olrw tcfh set
> jkm m st. tpwq buh gwxeedt pzht esf jrib mf yg mgsr ks crqwailp. ejty
> whw qeahztd ieqzsi zpzc sgbx gyx ghruc me oiotso! vi adv gbha pwsl,
> t'wm qkmo cbs on gyv pievr qwlttyl tbfalsoa wwfgyrzh bx sqyrvevn. eeoo
> shuc cgb'rp ytb srldywrg
> 
> x.l. loe xzwmk "qhmgyhcgr kkmr" lq zwyy rztl. lru krohol psacs tu anmi
> cbs quf.
> - nsrn pdgvfjrzdx
> 
> brassg{lhrrfxzgxvrpzmierkrkdbkdyeibpredxbrflvvvotgvfisacb}
> 
> eiie sisj ga bwvi, knq lrw gulj l rigwej yf glux tlfzcf xnmt jvlr imx
> aro v dk. xwsl esj orqejkl jkim loe qwbk oa vw fmch sw tysflzpw. aeww
> ypr jeforno jxxvrp eiie ndrq min olibe vp fmvpnr! tk iyo ggos jhte,
> a'sl xpfx ewp eg mil xmvct zhcxaug wzhiglof dozrzkgd ae xjhtqblg. koew
> wybe lrs'vw uoe qttyrwwn
> 
> p.f. wpx evvtp "jqobvxvmb asqi" ss ihpc yvoo. jtc fkomvd jdbvz pt hsfr
> ewp gnl.
> - xizr gkieqavgzs

## Solving
The format of the ciphertext and intact punctuation immediately suggests some sort of substitution type cipher. These two segments in particular look like the flag format of texsaw{orthogonal}:

	twhsnz{tngqmqdhqqygxrloyehuvxtwwvxklkiiudpxqcvqhbmkepledu}
	brassg{lhrrfxzgxvrpzmierkrkdbkdyeibpredxbrflvvvotgvfisacb}



If we apply a vigenere decoder with key "texsaw" to "twhsnz" and "brassg", we get

	askand
	indask

We now know that the key starts with "askand", and contains"indask". When using a key with a vigenere cipher, if the plaintext is longer than the key, typically the key is just repeated. For example, if the key is "thisisverysecret" ...
	
	thisisverysecretthisisverysecretthisisverysecret.....
... the plaintext would be encrypted using the above.

Knowing this, we can guess that the "ask" in "indask" is actually the beginning of a repetition, and that the key ends in "ind". 

Each of the two messages have 366 encodeable characters (a-z). Since we believe "ind" is the end of the key, that means that 
	
	(366+3) % key_length = 0
369 = 3**2 * 41, so possible values of key_length are
	
	1
	3
	9
	41
	123
When testing a key length of 41, 
	
	key= askandaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaind
we get the following:

> **texsaw**{tngqmqdhqqygxrloyehuvxtwwvxklkii**mqmxysvde**bmkepledu}
> 
> zpzc xlcq aq lorr, dlh aas zyq**y a matter o**n mate mpgsxm olrw tcfh
> set jkm m st. tpwq **the genera**t pzht esf jrib mf yg mgsr ks
> crqwailp. ej**ll the gene**ztd ieqzsi zpzc sgbx gyx ghruc me oiots**g!
> if all goe**a pwsl, t'wm qkmo cbs on gyv pievr qwlttyl **location
> t**wfgyrzh bx sqyrvevn. eeoo shuc cgb'rp yt**t followed**
> 
> x.l. loe xzwmk "qhmgyhcgr kkmr" lq zwyy rzt**d. you shoul**l psacs tu
> anmi cbs quf.
> - nsrn pdgvfjrzdx
> 
> **texsaw{luo**rfxzgxvrpzmierkrkdbkdyeibpredxbr**xysvdetts**fisacb}
> 
> eiie sisj ga bwvi, knq lrw gulj l r**atter of ti**ux tlfzcf xnmt jvlr
> imx aro v dk. xwsl esj **general wh**im loe qwbk oa vw fmch sw
> tysflzpw. aeww y**he general** jxxvrp eiie ndrq min olibe vp fmvpnr!
> tk **all goes we**te, a'sl xpfx ewp eg mil xmvct zhcxaug wzh**ation
> tomo**zkgd ae xjhtqblg. koew wybe lrs'vw uoe qt**llowed p.s. t**px
> evvtp "jqobvxvmb asqi" ss ihpc yvoo. jt**u should wa**bvz pt hsfr ewp
> gnl.
> - xizr gkieqavgzs

Using the context from the message, and from internet search, one can eventually conclude the key is
	
	askanditshallbegivenyouseekandyeshallfind
Which will give us the plaintext with the flag

> texsaw{luojmfsgmkqltenaemdqlxgtyrfdlzxdmqmxysvdettsxpatcq}
> 
> they know im here, and its only a matter of time before they find out
> who i am. tell the general what the flag is as soon as possible. tell
> the general before they find out where im hiding! if all goes well,
> i'll meet you at our first meeting location tomorrow at midnight. make
> sure you're not followed
> 
> p.s. the movie "imitation game" is very good. you should watch it when
> you can.
> - john cairncross
> 
> texsaw{luojmfsgmkqltenaemdqlxgtyrfdlzxdmqmxysvdettsxpatcq}
> 
> they know im here, and its only a matter of time before they find out
> who i am. tell the general what the flag is as soon as possible. tell
> the general before they find out where im hiding! if all goes well,
> i'll meet you at our first meeting location tomorrow at midnight. make
> sure you're not followed
> 
> p.s. the movie "imitation game" is very good. you should watch it when
> you can.
> - john cairncross





## Alternate Solve
The title of the challenge, "The Imitation Game", is a movie about Alan Turing and the enigma machine. In the movie, one of the characters is a soviet spy, and encrypts his message using Matthew 7:7 as the key. Knowing this makes solving much faster.



