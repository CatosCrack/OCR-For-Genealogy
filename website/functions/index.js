require("dotenv").config(); // Load environment variables from .env file

// onRequest handles HTTP requests
const {onRequest} = require("firebase-functions/v2/https");
const cors = require("cors");

// logger is used to send log messages to cloud logging
const logger = require("firebase-functions/logger");

// Import Firebase Admin SDK to access Firestore
// {} is used to destructuture the required functions from the Firebase Admin SDK
// e.g.: Instead of const firebase = require("firebase-admin/app"); and then const initializeApp = firebase.initializeApp;
const {initializeApp} = require("firebase-admin/app");
const {getFirestore} = require("firebase-admin/firestore");

// Get express app to setup server
const express = require("express");
const session = require("express-session");
const app = express();

// Request middleware
app.use(cors({ origin: true }))
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded form data
app.use(express.json()); // Parse JSON data
app.use(express.static("public")); // Serve static files from the public directory
app.use(session({
    secret: process.env.SESSION_KEY,
    resave: false,
    saveUninitialized: false,
    cookie: {                    // <-- This is the 'cookie' parameter
        secure: process.env.NODE_ENV === 'production',
        maxAge: 24 * 60 * 60 * 1000
    }
}));

// Initialize apps
initializeApp();
const db = getFirestore();

// Server paths
app.get("/", (req, res) => {
    res.sendFile("index.html", { root: "public" });
});

app.post("/search", async (req, res) => {

    // Get the first and last name from the form request
    const firstName = req.body.fname;
    const lastName = req.body.lname;
    logger.log(`Searching for: ${firstName} ${lastName}`);

    const results = await fetchResults(firstName, lastName, res);
    if (req.session.results) {
        req.session.results = []; // Clear previous results
        req.session.results = results; // Store new results in session
    } else {
        req.session.results = results; // Store results in session
    }
    
});

// Define search function
async function fetchResults(fname, lname, res){
    try {
        var resultArray = [];

        // Get the bounds snapshots from Firestore
        const boundsSnapshots = await db.collection('Bounds')
            .where("first_name", "==", fname)
            .where("last_name", "==", lname)
            .get();

        // Extract document data
        for (const result of boundsSnapshots.docs) {
            const data = result.data();
            const fname = data["first_name"];
            const lname = data["last_name"];
            const docId = data["doc_id"];
            const boundsId = result.id; // This ID will be used to get the bounds from the viewer script

            // Fetch the document data from the Document collection
            const documentSnapshot = await db.collection('Document').doc(docId).get();
            const docData = documentSnapshot.data();
            const url = docData["url"];
            const municipality = docData["municipality"];
            const department = docData["department"];
            const year = docData["year"];

            // Create person object to include in resultArray
            var person = {
                name: fname + ' ' + lname,
                boundsId: boundsId,
                municipality: municipality,
                department: department,
                year: year,
                url: url
            }

            // Add person to resultArray
            resultArray.push(person);
        }

        return resultArray;

    } catch {
        logger.error("Error fetching results:", error);
        res.status(500).send("Error fetching results");
    }
}


