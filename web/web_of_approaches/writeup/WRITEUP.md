# Web of Approaches Writeup

The webpage on the surface contains nothing but a quiz. The quiz in its current state is impossible due to question 3:

"Which HTML tag is used to define content that is only displayed if the CSS fails to load or is disabled?"

No such tag exists, so trying to submit any answers will give the feedback:

"Incorrect Answers. Please ensure all existing questions have a correct answer."

Which is a hint that you need to remove the question from the page before submitting it to get the part of the encoded flag.

Opening the page with inspect element and deleting the third question then submitting the correct answers for the rest of them (or just deleting all the questions) will give you one part of the encoded flag, which appears to be in base64. You will also notice that the content of the html is complete gibberish because the page has a custom font that acts as effectively a substitution cipher. This cipher will have to be applied to all parts of the base64 flags to be able to decipher them into the actual flag.

In the CSS you will also find that the background, despite being entirely white, is a custom repeating image. Looking at the image itself you can see that it's white but the opacity of each pixel is different. Taking the hex value of each pixel and converting it to ascii (left to right, top to bottom) gives another base64 string.

Looking at the script.js file, you can see that on the document loading the javascript modifies an element with an id that through the substitution cipher translates to "flag-segment" (this is to make it so you can't just look at the initial html page to find the segment), and later on deletes that element when a certain trigger defined by the other js file occurs. This trigger is the script detecting the browser console being open. To get the segment, you can reload the page without opening the browser console and simply copy the area of the web page where the element initally loads, as the text is just set to font-size 0 instead of being properly hidden.

Once all parts of the flag have been collected and put through the substitution cipher, they will each give a message that isn't the flag but shows which order they go in depending on the word number in the string. Each string is split up into a bunch of smaller string with a lot of padding, with the bits of the flag being hidden in the padding that isn't used when the string is converted to ascii. Extracting these bits and converting them to ascii will give the inside of the flag, and putting it in the proper format (texsaw{...}) will give the flag.