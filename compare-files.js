import fs from 'fs'
import path from 'path'

const mergeSmallerFileToCombined = (oldDir, newDir, combinedDir) => {
  const oldFiles = fs.readdirSync(oldDir).map(file => path.join(oldDir, file));
  const newFiles = fs.readdirSync(newDir).map(file => path.join(newDir, file));
  
  for (const oldFile of oldFiles) {
    const oldSize = fs.statSync(oldFile).size;
    const oldFileName = oldFile.split('/').pop();
  
    for (const newFile of newFiles) {
      const newSize = fs.statSync(newFile).size;
      const newFileName = newFile.split('/').pop();
  
      if (oldFileName != newFileName) {
        continue
      }
  
      const combinedFile = path.join(combinedDir, oldFileName);

      if (oldSize <= newSize) {
        fs.copyFile(oldFile, combinedFile, (err) => {
          if (err) throw err;
          console.log(`Copy ${oldFile} to ${combinedDir}`);
        })
      } else {
        fs.copyFile(newFile, combinedFile, (err) => {
          if (err) throw err;
          console.log(`Copy ${newFile} to ${combinedDir}`);
        })
      }
    }
  }
}

mergeSmallerFileToCombined(
  '/home/hynksy/Videos/old/2020', 
  '/home/hynksy/Videos/new/2020',
  '/home/hynksy/Videos/combined/2020')