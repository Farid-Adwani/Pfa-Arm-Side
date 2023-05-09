import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';

declare var apiRTC: any;


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  title = 'ApiRTC-angular';

  constructor(private fb: FormBuilder) {
  }
  ngOnInit(): void {
    this.getOrcreateConversation()
  }


  getOrcreateConversation() {
    var localStream: any;

    // CREATE USER AGENT
    var ua = new apiRTC.UserAgent({
      uri: 'apzkey:myDemoApiKey'
    });

    // REGISTER
    ua.register().then((session: { getConversation: (arg0: any) => any; }) => {

      // CREATE CONVERSATION
      const conversation = session.getConversation(1234);

      // CREATE LOCAL STREAM
      ua.createStream({
        constraints: {
          audio: false,
          video: true
        }
      })
        .then((stream: any) => {

          console.log('createStream :', stream);

          // Save local stream
          localStream = stream;
          stream.removeFromDiv('local-container', 'local-media');
          stream.addInDiv('local-container', 'local-media', {}, true);

          // JOIN CONVERSATION
          conversation.join()
            .then((response: any) => {

              // PUBLISH LOCAL STREAM
              conversation.publish(localStream);
            }).catch((err: any) => {
              console.error('Conversation join error', err);
            });

        }).catch((err: any) => {
          console.error('create stream error', err);
        });
    });
  }
}
