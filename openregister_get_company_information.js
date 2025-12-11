import Openregister from 'openregister';
import 'dotenv/config';
import fs from 'fs';

const client = new Openregister({
apiKey: process.env.OPEN_REGISTER_API_KEY,
});

const company_id = 'DE-HRB-M1201-43507';
const response = await client.company.getDetailsV1(company_id);

const output = JSON.stringify(response, null, 2);

const title = "openregister_get_company_information";
const filename = `${title}_${company_id}.txt`;

// write to file
fs.writeFileSync(filename, output);

//console.log(response);