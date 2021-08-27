async function fetchFile(file) {
    // Return an array of the data, each element is a line
    let x = await fetch(file);
    let y = await x.text();
    return y.split("\r\n");
}
// Initialize prevLen once
fetchFile("Belt.txt").then(function(result) {prevLen = result.length;});
// Update the time every second
let clock = setInterval(function() {document.getElementById("Date").innerHTML =
        new Date();}, 1000);

let real_min = 0;  // Keep track of the minutes passed since activation
let prevLen;  // Stores the previous length of the log file
let isSmoove;  // Will be a boolean, true is movement, false is stop
let progressBars = setInterval(function() {
    // Update the progress bars every minute
    function isHalt(data) {return Number(data) === 3 ? true : false;}
    // Return if the data is 3 or 0/1
    
    ++real_min;
    if (real_min === 630) {
        // Stop both setInterval functions after 10.5 hours
        clearInterval(clock);
        clearInterval(progressBars);
    }

    fetchFile("Belt.txt").then(function(result) {
        // Change isSmoove based on activity from the past minute
        let curLen = result.length;
        if (curLen - prevLen <= 10) {isSmoove = false;}
        // The line has halted if there are few new entries
        else {
            let newEntries = curLen - prevLen;
            let mEntry = skip = 0;  // mEntry is amount of moving entries, skip is amount of invalid lines
            for (let i = 1; i <= newEntries; ++i) {
                // For every new entry
                switch (result[-i].length) {
                    case 0:  // Empty line
                        ++skip;
                        break;
                    case 1:  // Either a session header or starting 3
                        break;
                    case 2:  // First move entry
                        if (!isHalt(result[-i][0])) {++mEntry;}
                        break;
                    case 4:  // The entry after a first move entry
                        if (!isHalt(result[-i][26])) {++mEntry;}
                        break;
                    default:  // Standard entry: timestamp, data, passed secconds
                        if (!isHalt(result[-i][13])) {++mEntry;}
                }
            }
            newEntries -= skip;  // Readjust the difference
            isSmoove = mEntry / newEntries >= 0.80 ? true : false;
        }
    })

    let moveBar = document.getElementById("Move");
    let stopBar = document.getElementById("Stop");
    let moveTime = Number(moveBar.getAttribute("value"));
    let stopTime =  Number(stopBar.getAttribute("value"));
    if (isSmoove) {
        ++moveTime;
        moveBar.setAttribute("value", moveTime);
        document.getElementById("mLabel").innerHTML = `Minutes Running: ${moveTime}`;
    }
    else {
        ++stopTime;
        stopBar.setAttribute("value", stopTime);
        document.getElementById("sLabel").innerHTML = `Minutes Halted: ${stopTime}`;
    }

    let ratio = (1 - (stopTime / moveTime)) * 100;
    document.getElementById("ratio").innerHTML = `Uptime ratio: ${ratio}%`;
}, 1000);