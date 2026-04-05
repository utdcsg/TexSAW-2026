# My First Website Writeup

### Gathering Information

The first thing to notice is the `/login` page linked on the homepage. When we visit it, we can see that it consists of a form with a username and password. Entering any combination, it redirects us to the homepage.

Notice that by logging in, the website saves a JWT (JSON Web Token) cookie that it uses for authentication. It is stored in Base64.

I entered "test" and "test password" into the fields. By converting the JWT to plaintext using CyberChef, I get something that looks like this:
`{"alg":"HS256","typ":"JWT"}{"username":"test","password":"test password","iat":1769806699}M@Òí9(ÚÆKãwÜü¿PebûL¿/s3ª`

By doing a little research, we notice this is a pretty standard format for JWTs, where there are three fields separated by a period `.`
* Header
* Payload
* Signature

The JWT signs the payload by using a private key, ensuring the payload came from a trusted source.

### Trying different payloads

Since we can't directly spoof a JWT, what if we try customizing the payload? Clearly the login page is what gave us the JWT, let's play around with it.

By using browser developer tools or any tool for sending requests, if we send an arbitrary payload as the form data on the login page like `"randomkey=test"`, this is what the JWT looks like (the private key is random, so the signature may differ)
`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyYW5kb21rZXkiOiJ0ZXN0IiwiaWF0IjoxNzY5ODEzMzUxfQ.-gtgP5Un4cGuFzuRPfQ0M9OvkzQGfjcXs5rw2KAv7So`
```js
// The request in browser console
fetch("http://localhost:3000/login", {
  "headers": {
    "content-type": "application/x-www-form-urlencoded"
  },
  "body": "randomkey=test",
  "method": "POST"
});
```

When decoded from Base64, we get
`{"alg":"HS256","typ":"JWT"}{"randomkey":"test","iat":1769813351}-þT¸\îD÷ÐÐÏN¾LÐøÜ^ÎkÃb¿´¨`

Notice that the payload matches what we sent, meaning we can inject arbitrary data into our JWT.

### Finding the flag

If we visit `/robots.txt`, this is what we find:
```
User-agent: *
Disallow: /admin
```

Curiously visiting `/admin` results in a page saying "You are not an admin" and giving a link for the admin login. No matter what we try for the admin login, nothing works.

What if we inspect the admin page? There is nothing suspicious on `/admin`, but on `/admin/login`, there is a commented out script checking `if (username == 'admin' && isAdmin == true)`

Naturally, let's try that as our payload, using the following request:
```js
// Try using the key-value pairs we found
fetch("http://localhost:3000/login", {
  "headers": {
    "content-type": "application/x-www-form-urlencoded"
  },
  "body": "username=admin&isAdmin=true",
  "method": "POST"
});
```

Now, if we visit `/admin`, it displays the flag!