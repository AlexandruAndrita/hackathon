import Openregister from 'openregister';
import 'dotenv/config';
import fs from 'fs';

const client = new Openregister({
apiKey: process.env.OPEN_REGISTER_API_KEY,
});

// "Hannelore Eberz";
const person_id = 'cc302aad-6e26-4140-8fba-10bae1c3c434';
const response = await client.person.getDetailsV1(person_id);

const output = JSON.stringify(response, null, 2);
    
const title = `openregister_person_information`;
const filename = `${title}_${person_id}.txt`;

fs.writeFileSync(filename, output);