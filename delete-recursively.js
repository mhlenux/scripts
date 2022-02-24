import fs from 'fs'
import path from 'path'

/**
 * Delete recursively (by regex pattern)
 * @param {*} dir 
 * @param {*} pattern regex
 */
const deleteRecursively = (dir, pattern) => {
    let files = fs.readdirSync(dir).map(file => path.join(dir, file));
    for(let file of files) {
        const stat = fs.statSync(file);
        if (stat.isDirectory()) {
            deleteRecursively(file, pattern);
        } else {
            if (pattern.test(file)) {
                console.log(`Deleting file: ${file}...`);
                // Uncomment the next line once you're happy with the files being logged!
                try {
                    // Comment this WHEN DONE!
                    //fs.unlinkSync(file);
                } catch (err) {
                    console.error(`An error occurred deleting file ${file}: ${err.message}`);
                }
            }
        }
    }
}

deleteRecursively('/home/hynksy/Pictures', /\.mp4$/);
