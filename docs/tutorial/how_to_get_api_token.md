!!! abstract

    This page shows the steps to acquiring an API Token to connect to the [CRIPT platform](https://criptapp.org)

<br/>

The token is needed because we need to authenticate the user before saving any of their data

!!! Warning "Token Security"
      It is **highly** recommended that you store your API tokens in a safe location and read it into your code
      Hard-coding API tokens directly into the code can pose security risks,
      as the token might be exposed if the code is shared or stored in a version control system.

      Anyone that has access to your tokens can impersonate you on the [CRIPT platform](https://criptapp.org)

<img class="screenshot-border" src="../../images/cript_token_page.png" alt="Screenshot of CRIPT security page where API token is found">

<small>
   [Security Settings](https://app.criptapp.org/security)
   under the profile icon dropdown
</small>


To get your token:

1. please visit your [Security Settings](https://app.criptapp.org/security) under the profile
   icon dropdown on the top right
2. Click on the **copy** button next to the API Token to copy it to clipboard
3. Now you can paste it into the `API Token` field

Example:

<!-- trunk-ignore-begin(cspell/error) -->
<!-- trunk-ignore-begin(gitleaks/jwt) -->

```yaml
API Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

Storage Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gU21pdGgiLCJpYXQiOjE1MTYyMzkwMjJ9.Q_w2AVguPRU2KskCXwR7ZHl09TQXEntfEA8Jj2_Jyew
```

<!--  trunk-ignore-end(gitleaks/jwt) -->
<!--  trunk-ignore-end(cspell/error) -->
