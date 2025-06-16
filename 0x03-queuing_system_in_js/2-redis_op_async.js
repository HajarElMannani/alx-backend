import { createClient, print } from "redis";
import { promisify } from "util";

const client = createClient();
client.on('connect', () => {
  console.log("Redis client connected to the server");
});
client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print);
}

async function displaySchoolValue(schoolName) {
  try {
    const reply = await promisify(client.get).bind(client)(schoolName);
    console.log(reply);
  }
  catch (err) { 
      console.log(err);
  }
}
(async () => {  
await displaySchoolValue('ALX');
setNewSchool('ALXSanFrancisco', '100');
await displaySchoolValue('ALXSanFrancisco');
})();
