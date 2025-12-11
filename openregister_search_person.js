import Openregister from 'openregister';
import 'dotenv/config';
import fs from 'fs';

const client = new Openregister({
apiKey: process.env.OPEN_REGISTER_API_KEY,
});

const person_name = "Hannelore Eberz";
const response = await client.search.findPersonV1({
    query:{
        value: person_name
    }
});

const output = JSON.stringify(response, null, 2);
    
const title = `openregister_person_search`;
const filename = `${title}_${person_name}.txt`;

fs.writeFileSync(filename, output);