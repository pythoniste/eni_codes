            try {
                var autobahn = require('autobahn');
            } catch (e) {
                console.log("when running in browser, AutobahnJS will be included without a module system");
            }

            var connection = new autobahn.Connection({
                url: 'ws://127.0.0.1:8080/ws',
                realm: 'test'}
            );

            connection.onopen = function (session) {
                function on_clock_event(args) {
                    document.getElementById("clock").innerText=args[0];
                    console.log("Message received: ", args[0]);
                }
                session.subscribe('com.test.topic_clock', on_clock_event);
            };

            //load_clock = function() {
                connection.open();
            //};
/*
            window.onload = function() {
                setTimeout(load_clock, 10000);
            };

            window.onbeforeunload = function (e) {
                document.getElementById("clock").innerText="Clock";
                console.log("Closing ..");
                connection.close();
            }
*/
