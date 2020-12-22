import {promises as fs} from 'fs';
import amqplib from 'amqplib';
import path from 'path';
import ipfs from './ipfs.js';
import { exec } from 'child_process';

const main = async () => {
  const IPFS = await ipfs()
let conn = await amqplib.connect(process.env.MQ_URL || 'amqp://rabbitmq:rabbitmq@localhost')

let channel = await conn.createChannel();

let inQueue = process.env.MQ_QUEUE_IN
let outQueue = process.env.MQ_QUEUE_OUT

await channel.assertQueue(inQueue)
await channel.assertQueue(outQueue)

channel.consume(inQueue, async (msg) => {
  try{
    let json = JSON.parse(msg.content.toString())
    console.info("=> Processing: ", json.input_cid)
    await IPFS.getFile(json.input_cid, '/tmp/' + json.input_cid)


    //Run processor
    //
    exec(`${path.resolve('')}/step_to_gltf -o /tmp/${json.job_id} /tmp/${json.input_cid}`, async (err, stdout, stderr) => {
      if(err) {
        channel.nack(msg)
        return console.error(err)
      }

      console.log(err, stdout, stderr)

      let data = await fs.readFile(`/tmp/${json.job_id}`)
      let result = await IPFS.addFile(data)

      channel.sendToQueue(outQueue, Buffer.from(JSON.stringify({
        job_id: json.job_id,
        input_cid: result.toString()
      })))
      channel.ack(msg)
    })

  }catch(e){
    console.error(e)
  }
})
}
main()
