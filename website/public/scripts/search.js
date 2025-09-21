// Get database
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js";
import { getFirestore, collection, query, where, getDocs, doc, getDoc } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "YOUR_KEY",
    authDomain: "YOUR_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_BUCKET",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Get form submission data
document.getElementById('search').addEventListener('submit', async function (event) {
    event.preventDefault();

    // Get names
    const firstName = document.getElementById('fname').value;
    const lastName = document.getElementById('lname').value;

    // console.log("Name: " + firstName + " " + lastName);

    // Fetch results
    await fetchResults(firstName, lastName);
});

async function fetchResults(firstName, lastName) {
    const firstName = "Antonio Jose"
    const lastName = "Herrera";
    console.log("Fetching results...");
    try{
        // Create a javascript object to store the results
        var resultArray = [];

        // Get all bound snapshots
        const boundsSnapshots = await getDocs(query(collection(db, 'Bounds'), 
                                                        where("first_name", "==", firstName), 
                                                        where("last_name", "==", lastName)));

        // Add results to the resultArray
        for (const result of boundsSnapshots.docs){
            // Gather bounds data
            const resultData = result.data();
            const bounds = resultData["bounds"];
            const first_name = resultData["first_name"];
            const last_name = resultData["last_name"];

            // Get document data
            const doc_id = resultData["doc_id"];
            const document = await getDoc(doc(db, 'Document', doc_id));
            const docData = document.data();
                                
            const url = docData["url"];
            const municipality = docData["municipality"];
            const department = docData["department"];
            const year = docData["year"];

            // Create person object to include in resultArray
            var person = {
                name: first_name + ' ' + last_name,
                bounds: bounds,
                municipality: municipality,
                department: department,
                year: year,
                url: url
            }

            // console.log(person);
                
            resultArray.push(person);
        }

        //Save results
        sessionStorage.setItem('results', JSON.stringify(resultArray));
        window.location.href = 'result_page.html';

    } catch (error) {
        console.error("Error fetching data: ", error);
    }
}