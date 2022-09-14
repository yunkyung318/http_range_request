"use strict";

const express = require("express");
const app = express();
const fs = require("fs");
const path = require('path');

app.get("/", function (req, res) {
	const file = __dirname + '/text.txt';
	const filePath = path.basename(file);
	const filesize = fs.statSync(file).size;
	
	res.send(filesize+"\n");
});

app.get("/text", function (req, res) {
	const range = req.headers.range;
    	console.log(range);
	if (!range) {
		res.status(400).send("Requires Range header");
    	}
	
	const file = __dirname + '/text.txt';
	const filePath = path.basename(file);
	const filesize = fs.statSync(file).size;
    
	const full_ran = range.split('-');
	
	const start = Number(full_ran[0]);
	const end = Number(full_ran[1]);

	//const contentLength = end - start + 1;
    	//const headers = {
		//"Content-Range": `${start}-${end}/${filesize}`,
        	//"Accept-Ranges": "bytes",
        	//"Content-Length": contentLength,
        	//"Content-Type": "txt",
	//};
    	//res.writeHead(206, headers);
	
	//setTimeout(() =>{ 
	res.write(filesize+"\n");
    		
	const fileStream = fs.createReadStream(filePath, { start, end });
	fileStream.pipe(res);
		
	console.log("Text Range Succes");
});

/*
app.get("/image", function (req, res) {
	const range = req.headers.range;
    	console.log(range);
	if (!range) {
		res.status(400).send("Requires Range header");
    	}
	
	const file = __dirname + '/Lenna.png';
	const filePath = path.basename(file);
	const filesize = fs.statSync(file).size;
    
	const full_ran = range.split('-');
	
	const start = Number(full_ran[0]);
	const end = Number(full_ran[1]);

	//const contentLength = end - start + 1;
    	//const headers = {
	//	"Content-Range": `bytes ${start}-${end}/${filesize}`,
        //	"Accept-Ranges": "bytes",
        //	"Content-Length": contentLength,
        //	"Content-Type": "txt",
	//};

    	//res.writeHead(206, headers);
	res.write(filesize+"\n");

    	const fileStream = fs.createReadStream(filePath, { start, end });
	fileStream.pipe(res);
	
	console.log("Image Range Succes");

});
*/
app.listen(8000, function () {
    console.log("Listening on port 8000!");
});
