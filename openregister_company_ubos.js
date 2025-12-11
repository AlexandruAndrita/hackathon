/**
 * works only for the following legal forms:
 * - GmbH      ("gmbh")
 * - GGmbH     ("ggmbh")
 * - KG        ("kg")
 * - UG        ("ug")
 */

import Openregister from 'openregister';
import 'dotenv/config';
import fs from 'fs';

const client = new Openregister({
apiKey: process.env.OPEN_REGISTER_API_KEY,
});

const company_ids = ['DE-HRB-M1201-128843', 'DE-HRB-M1201-43507'];

for (const company_id of company_ids) {
    const response = await client.company.getUbosV1(company_id);

    const output = JSON.stringify(response, null, 2);

    const title = "openregister_get_company_ubos";
    const filename = `${title}_${company_id}.txt`;

    fs.writeFileSync(filename, output);
}

