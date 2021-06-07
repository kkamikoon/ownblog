## Code Test
```
<html>
  <head>
      <title>
          Vue.js Pet Shop
      </title>
      <script src="https://unpkg.com/vue@2.5.2"></script>
      <link   rel="stylesheet"
              type="text/css"
              href="assets/css/app.css"/>
      <!-- <link   rel="stylesheet"
              href="https://maxcnd.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
              crossorigin="anonymouse"> -->
  </head>
  <body>
      <!-- Mount the Vue here -->
      <div id="app">
          <header>
              <h1 v-text="sitename"></h1>
          </header>
      </div>
      <script type="text/javascript">
          var webstore = new Vue({    // Vue initiate
              el: "#app",             // The Vue can find where it can mount on DOM. It is CSS Selector(?)
              data: {
                  sitename: "Vue.js Pet Shop"
              }
          });
      </script>
  </body>
</html>
```

- this is Vue.js Code