const express = require('express');

const app = express();
const port = 8181;




app.get('/', (req, res) => {
	res.send("<html><body><center><h1><marquee>Welcome to TailsNet!</marquee></h1></center></body></html>");
});

app.listen(port, () => {
	console.log('Listening');
});
