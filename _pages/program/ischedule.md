---
title: Schedule
layout: schedule
excerpt: "EMNLP-IJCNLP 2019 Conference Schedule."

permalink: /program/ischedule/
sidebar: false
script: |
    <script type="text/javascript">

        sessionInfoHash = {};
        paperInfoHash = {};
        chosenPapersHash = {};
        chosenTutorialsHash = {};
        chosenWorkshopsHash = {};
        chosenPostersHash = {};
        plenarySessionHash = {};
        includePlenaryInSchedule = true;
        helpShown = false;

        var instructions = "<div id=\"popupInstructionsDiv\"><div id=\"title\">Help</div><div id=\"popupInstructions\"><ul><li>Click on a the \"<strong>+</strong>\" button or the title of a session to toggle it. Click the <strong>\"Expand All Sessions ↓\"</strong> button to expand <em>all</em> sessions in one go. Click again to collapse them. </li> <li>Click on a tutorial/paper/poster to toggle its selection. </li> <li>You can select more than one paper for a time slot. </li> <li>Click the &nbsp;<i class=\"fa fa-file-pdf-o\" aria-hidden=\"true\"></i>&nbsp; /&nbsp;<i class=\"fa fa-file-video-o\" aria-hidden=\"true\"></i>&nbsp; icon(s) for the PDF / Video. </li> <li>Click the <strong>\"Download PDF\"</strong> button at the bottom to download your customized PDF. </li> <li>To expand parallel sessions simultaneously, hold Shift and click on any of them. </li> <li>On non-mobile devices, hovering on a paper for a time slot highlights it in yellow and its conflicting papers in red. Hovering on papers already selected for a time slot (or their conflicts) highlights them in green. </li> <li>Hover over the time for any session to see its day and date as a tooltip.</li> <li>While saving the generated PDF on mobile devices, its name cannot be changed.</li> </ul></div></div>";

        function padTime(str) {
            return String('0' + str).slice(-2);
        }

        function formatDate(dateObj) {
            return dateObj.toLocaleDateString() + ' ' + padTime(dateObj.getHours()) + ':' + padTime(dateObj.getMinutes());
        }

        function generatePDFfromTable() {

            /* clear the hidden table before starting */
            clearHiddenProgramTable();

            /* now populate the hidden table with the currently chosen papers */
            populateHiddenProgramTable();

            var doc = new jsPDF('l', 'pt', 'letter');
            doc.autoTable({
                fromHtml: "#hidden-program-table",
                pagebreak: 'avoid',
                avoidRowSplit: true,
                theme: 'grid',
                startY: 70, 
                showHead: false,
                styles: {
                    font: 'times',
                    overflow: 'linebreak',
                    valign: 'middle',
                    lineWidth: 0.4,
                    fontSize: 11
                },
                 columnStyles: {
                    0: { fontStyle: 'bold', halign: 'right', cellWidth: 70 },
                    1: { cellWidth: 110 },
                    2: { fontStyle: 'italic', cellWidth: 530 }
                },
                addPageContent: function (data) {
                    /* HEADER only on the first page */
                    var pageNumber = doc.internal.getCurrentPageInfo().pageNumber;

                    if (pageNumber == 1) {
                        doc.setFontSize(16);
                        doc.setFontStyle('normal');
                        doc.text("EMNLP 2018 Schedule", (doc.internal.pageSize.width - (data.settings.margin.left*2))/2 - 30, 50);
                    }

                    /* FOOTER on each page */
                    doc.setFont('courier');
                    doc.setFontSize(8);
                    doc.text('(Generated via http://emnlp2018.org/schedule)', data.settings.margin.left, doc.internal.pageSize.height - 10);
                },
                drawCell: function(cell, data) {
                    var cellClass = cell.raw.content.className;
                    /* center the day header */
                    if (cellClass == 'info-day') {
                        cell.textPos.x = (530 - data.settings.margin.left)/2 + 120;
                    }
                    /* split long plenary session text */
                    else if (cellClass == 'info-plenary') {
                        cell.text = doc.splitTextToSize(cell.text.join(' '), 530, {fontSize: 11});
                    }
                },
                createdCell: function(cell, data) {
                    var cellClass = cell.raw.content.className;
                    var cellText = cell.text[0];
                    /* */
                    if (cellClass == 'info-day') {
                        cell.styles.fontStyle = 'bold';
                        cell.styles.fontSize = 12;
                        cell.styles.fillColor = [187, 187, 187];
                    }
                    else if (cellClass == 'info-plenary') {
                        cell.styles.fontSize = 11;
                        if (cellText == "Break" || cellText == "Lunch" || cellText == "Breakfast" || cellText == "Coffee Break") {
                            cell.styles.fillColor = [238, 238, 238];
                        }
                    }
                    else if (cellClass == 'info-poster') {
                        cell.styles.fontSize = 9;
                    }
                    else if (cellClass == "location") {
                        if (cellText == '') {
                            var infoType = data.row.raw[2].content.className;
                            if (infoType == "info-day") {
                                cell.styles.fillColor = [187, 187, 187];
                            }
                            else if (infoType == "info-plenary") {
                                cell.styles.fillColor = [238, 238, 238];
                            }
                        }
                    }
                    else if (cellClass == "time") {
                        var infoType = data.row.raw[2].content.className;
                        var infoText = data.row.raw[2].content.textContent;
                        if (infoType == "info-day" && cellText == '') {
                            cell.styles.fillColor = [187, 187, 187];
                        }
                        if (infoType == "info-plenary" && (infoText == "Break" || infoText == "Lunch" || infoText == "Breakfast" || infoText == "Coffee Break")) {
                            cell.styles.fillColor = [238, 238, 238];
                        }
                    }
                },
            });
            doc.output('save');
        }

        function getTutorialInfoFromTime(tutorialTimeObj) {

            /* get the tutorial session and day */
            var tutorialSession = tutorialTimeObj.parents('.session');
            var sessionDay = tutorialSession.prevAll('.day:first').text().trim();

            /* get the tutorial slot and the starting and ending times */
            var tutorialTimeText = tutorialTimeObj.text().trim();
            var tutorialTimes = tutorialTimeText.split(' ');
            var tutorialSlotStart = tutorialTimes[0];
            var tutorialSlotEnd = tutorialTimes[2];
            var exactTutorialStartingTime = sessionDay + ' ' + tutorialSlotStart;
            return [new Date(exactTutorialStartingTime).getTime(), tutorialSlotStart, tutorialSlotEnd, tutorialSession.attr('id')];
        }

        function getWorkshopInfoFromTime(workshopTimeObj) {

            /* get the workshop session and day */
            var workshopSession = workshopTimeObj.parents('.session');
            var sessionDay = workshopSession.prevAll('.day:first').text().trim();

            /* get the workshop slot and the starting and ending times */
            var workshopTimeText = workshopTimeObj.text().trim();
            var workshopTimes = workshopTimeText.split(' ');
            var workshopSlotStart = workshopTimes[0];
            var workshopSlotEnd = workshopTimes[2];
            var exactworkshopStartingTime = sessionDay + ' ' + workshopSlotStart;
            return [new Date(exactworkshopStartingTime).getTime(), workshopSlotStart, workshopSlotEnd, workshopSession.attr('id')];
        }

        function getPosterInfoFromTime(posterTimeObj) {

            /* get the poster session and day */
            var posterSession = posterTimeObj.parents('.session');
            var sessionDay = posterSession.parent().prevAll('.day:first').text().trim();

            /* get the poster slot and the starting and ending times */
            var posterTimeText = posterTimeObj.text().trim();
            var posterTimes = posterTimeText.split(' ');
            var posterSlotStart = posterTimes[0];
            var posterSlotEnd = posterTimes[2];
            var exactPosterStartingTime = sessionDay + ' ' + posterSlotStart;
            return [new Date(exactPosterStartingTime).getTime(), posterSlotStart, posterSlotEnd, posterSession.attr('id')];
        }

        function isOverlapping(thisPaperRange, otherPaperRange) {
            var thisStart = thisPaperRange[0];
            var thisEnd = thisPaperRange[1];
            var otherStart = otherPaperRange[0];
            var otherEnd = otherPaperRange[1];
            return ((thisStart < otherEnd) && (thisEnd > otherStart));
        }

        function getConflicts(paperObject) {

            /* first get the parallel sessions */
            var sessionId = paperObject.parents('.session').attr('id').match(/session-\d/)[0];
            var parallelSessions = paperObject.parents('.session').siblings().filter(function() { return this.id.match(sessionId); });
            
            var thisPaperRange = paperInfoHash[paperObject.attr('paper-id')].slice(0, 2);
            return $(parallelSessions).find('table.paper-table tr#paper').filter(function(index) {
                    var otherPaperRange =  paperInfoHash[$(this).attr('paper-id')].slice(0, 2);
                    return isOverlapping(thisPaperRange, otherPaperRange) 
                });
        }

        function doWhichKey(e) {
            e = e || window.event;
            var charCode = e.keyCode || e.which;
            //Line below not needed, but you can read the key with it
            //var charStr = String.fromCharCode(charCode);
            return charCode;
        }

        function getConflicts2(paperObject) {

            /* most of the time, conflicts are simply based on papers having the same exact time slot but this is not always true */

            /* first get the conflicting sessions */
            var sessionId = paperObject.parents('.session').attr('id').match(/session-\d/)[0];
            var parallelSessions = paperObject.parents('.session').siblings().filter(function() { return this.id.match(sessionId); });
            
            /* now get the conflicting papers from those sessions */
            var paperTime = paperObject.children('td#paper-time')[0].textContent;
            return $(parallelSessions).find('table.paper-table tr#paper').filter(function(index) { return this.children[0].textContent == paperTime });

        }

        function makeDayHeaderRow(day) {
            return '<tr><td class="time"></td><td class="location"></td><td class="info-day">' + day + '</td></tr>';
        }

        function makePlenarySessionHeaderRow(session) {
            var sessionStart = session.start;
            var sessionEnd = session.end;
            return '<tr><td class="time">' + sessionStart + '&ndash;' + sessionEnd + '</td><td class="location">' + session.location + '</td><td class="info-plenary">' + session.title + '</td></tr>';
        }

        function makePaperRows(start, end, titles, sessions) {
            var ans;
            if (titles.length == 1) {
                ans = ['<tr><td class="time">' + start + '&ndash;' + end + '</td><td class="location">' + sessions[0].location + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
            }
            else {
                var numConflicts = titles.length;
                rows = ['<tr><td rowspan=' + numConflicts + ' class="time">' + start + '&ndash;' + end + '</td><td class="location">' + sessions[0].location + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
                for (var i=1; i<numConflicts; i++) {
                    var session = sessions[i];
                    var title = titles[i];
                    rows.push('<tr><td></td><td class="location">' + session.location + '</td><td class="info-paper">' + title + ' [' + session.title + ']</td></tr>')
                }
                ans = rows;
            }
            return ans;
        }

        function makeTutorialRows(start, end, titles, locations, sessions) {
            var ans;
            if (titles.length == 1) {
                ans = ['<tr><td class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
            }
            else {
                var numConflicts = titles.length;
                rows = ['<tr><td rowspan=' + numConflicts + ' class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
                for (var i=1; i<numConflicts; i++) {
                    var session = sessions[i];
                    var title = titles[i];
                    var location = locations[i];
                    rows.push('<tr><td></td><td class="location">' + location + '</td><td class="info-paper">' + title + ' [' + session.title + ']</td></tr>')
                }
                ans = rows;
            }
            return ans;
        }

    function makeWorkshopRows(start, end, titles, locations, sessions) {
            var ans;
            if (titles.length == 1) {
                ans = ['<tr><td class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
            }
            else {
                var numConflicts = titles.length;
                rows = ['<tr><td rowspan=' + numConflicts + ' class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
                for (var i=1; i<numConflicts; i++) {
                    var session = sessions[i];
                    var title = titles[i];
                    var location = locations[i];
                    rows.push('<tr><td></td><td class="location">' + location + '</td><td class="info-paper">' + title + ' [' + session.title + ']</td></tr>')
                }
                ans = rows;
            }
            return ans;
        }

        function makePosterRows(titles, types, sessions) {
            var numPosters = titles.length;
            var sessionStart = sessions[0].start;
            var sessionEnd = sessions[0].end;
            rows = ['<tr><td rowspan=' + (numPosters + 1) + ' class="time">' + sessionStart + '&ndash;' + sessionEnd + '</td><td rowspan=' + (numPosters + 1) + ' class="location">' + sessions[0].location + '</td><td class="info-paper">' + sessions[0].title +  '</td></tr>'];
            for (var i=0; i<numPosters; i++) {
                var title = titles[i];
                var type = types[i];
                /* rows.push('<tr><td></td><td></td><td class="info-poster">' + title + ' [' + type + ']</td></tr>'); */
                rows.push('<tr><td></td><td></td><td class="info-poster">' + title + '</td></tr>');
            }
            return rows;
        }

        function clearHiddenProgramTable() {
            $('#hidden-program-table tbody').html('');
        }

        function getChosenHashFromType(type) {
            var chosenHash;
            if (type == 'paper') {
                chosenHash = chosenPapersHash;
            }
            else if (type == 'tutorial') {
                chosenHash = chosenTutorialsHash;
            }
            else if (type == 'workshop') {
                chosenHash = chosenWorkshopsHash;
            }
            else if (type == 'poster') {
                chosenHash = chosenPostersHash;
            }
            return chosenHash;
        }

        function addToChosen(timeKey, item, type) {
            var chosenHash = getChosenHashFromType(type);
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                items.push(item);
                chosenHash[timeKey] = items;
            }
            else {
                chosenHash[timeKey] = [item];
            }
        }

        function removeFromChosen(timeKey, item, type) {
            var chosenHash = getChosenHashFromType(type);            
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                var itemIndex = items.map(function(item) { return item.title; }).indexOf(item.title);
                if (itemIndex !== -1) {
                    var removedItem = items.splice(itemIndex, 1);
                    delete removedItem;
                    if (items.length == 0) {
                        delete chosenHash[timeKey];
                    }
                    else {
                        chosenHash[timeKey] = items;
                    }
                }
            }
        }

        function isChosen(timeKey, item, type) {
            var ans = false;
            var chosenHash = getChosenHashFromType(type);
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                var itemIndex = items.map(function(item) { return item.title; }).indexOf(item.title);
                ans = itemIndex !== -1;
            }
            return ans;
        }

        function toggleSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideToggle(300);
            $(sessionObj).children('#expander').toggleClass('expanded');
        }

        function openSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideDown(300);
            $(sessionObj).children('#expander').addClass('expanded');
        }

        function closeSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideUp(300);
            $(sessionObj).children('#expander').removeClass('expanded');
        }

        function populateHiddenProgramTable() {

            /* since papers and posters might start at the same time we cannot just rely on starting times to differentiate papers vs. posters. so, what we can do is just add an item type after we do the concatenation and then rely on that item type to distinguish the item */
            
            var nonPlenaryKeysAndTypes = [];
            var tutorialKeys = Object.keys(chosenTutorialsHash);
            var workshopKeys = Object.keys(chosenWorkshopsHash);
            var posterKeys = Object.keys(chosenPostersHash);
            var paperKeys = Object.keys(chosenPapersHash);
            for (var i=0; i < tutorialKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([tutorialKeys[i], 'tutorial']);
            }
            for (var i=0; i < workshopKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([workshopKeys[i], 'workshop']);
            }
            for (var i=0; i < posterKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([posterKeys[i], 'poster']);
            }
            for (var i=0; i < paperKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([paperKeys[i], 'paper']);
            }

            var plenaryKeys = Object.keys(plenarySessionHash);
            var plenaryKeysAndTypes = [];
            for (var i=0; i < plenaryKeys.length; i++) {
                plenaryKeysAndTypes.push([plenaryKeys[i], 'plenary']);
            }

            /* if we are including plenary information in the PDF then sort its keys too and merge the two sets of keys together before sorting */
            var sortedPaperTimes = includePlenaryInSchedule ? nonPlenaryKeysAndTypes.concat(plenaryKeysAndTypes) : nonPlenaryKeysAndTypes;
            sortedPaperTimes.sort(function(a, b) { return a[0] - b[0] });

            /* now iterate over these sorted papers and create the rows for the hidden table that will be used to generate the PDF */
            var prevDay = null;
            var latestEndingTime;
            var output = [];

            /* now iterate over the chosen items */
            for(var i=0; i<sortedPaperTimes.length; i++) {
                var keyAndType = sortedPaperTimes[i];
                var key = keyAndType[0];
                var itemType = keyAndType[1]
                /* if it's a plenary session */
                if (itemType == 'plenary') {
                    var plenarySession = plenarySessionHash[key];
                    if (plenarySession.day == prevDay) {
                        output.push(makePlenarySessionHeaderRow(plenarySession));
                    }
                    else {
                        output.push(makeDayHeaderRow(plenarySession.day));
                        output.push(makePlenarySessionHeaderRow(plenarySession));
                    }
                    prevDay = plenarySession.day;
                }
                /* if it's tutorials */
                else if (itemType == 'tutorial') {

                    /* get the tutorials */
                    var tutorials = chosenTutorialsHash[key];

                    /* sort the tutorials by title instead of selection order */
                    tutorials.sort(function(a, b) {
                        return a.title.localeCompare(b.title);
                    });

                    var titles = tutorials.map(function(tutorial) { return ASCIIFold(tutorial.title); });
                    var locations = tutorials.map(function(tutorial) { return tutorial.location ; });
                    var sessions = tutorials.map(function(tutorial) { return sessionInfoHash[tutorial.session]; });
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makeTutorialRows(tutorials[0].start, tutorials[0].end, titles, locations, sessions));
                    prevDay = sessionDay;
                }
                /* if it's workshops */
                else if (itemType == 'workshop') {

                    /* get the workshops */
                    var workshops = chosenWorkshopsHash[key];

                    /* sort the workshops by title instead of selection order */
                    workshops.sort(function(a, b) {
                        return a.title.localeCompare(b.title);
                    });

                    var titles = workshops.map(function(workshop) { return ASCIIFold(workshop.title); });
                    var locations = workshops.map(function(workshop) { return workshop.location ; });
                    var sessions = workshops.map(function(workshop) { return sessionInfoHash[workshop.session]; });
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makeWorkshopRows(workshops[0].start, workshops[0].end, titles, locations, sessions));
                    prevDay = sessionDay;
                }
                /* if it's posters */
                else if (itemType == 'poster') {

                    /* get the posters */
                    var posters = chosenPostersHash[key];

                    /* sort posters by their type for easier reading */
                    posters.sort(function(a, b) {
                        return a.type.localeCompare(b.type);
                    });
                    var titles = posters.map(function(poster) { return ASCIIFold(poster.title); });
                    var types = posters.map(function(poster) { return poster.type; });
                    var sessions = [sessionInfoHash[posters[0].session]];
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makePosterRows(titles, types, sessions));
                    prevDay = sessionDay;
                }

                /* if it's papers  */
                else if (itemType == 'paper') {
                    var papers = chosenPapersHash[key];
                    /* sort papers by location for easier reading */
                    papers.sort(function(a, b) {
                        var aLocation = sessionInfoHash[a.session].location;
                        var bLocation = sessionInfoHash[b.session].location;
                        return aLocation.localeCompare(bLocation);
                    });
                    var titles = papers.map(function(paper) { return ASCIIFold(paper.title); });
                    var sessions = papers.map(function(paper) { return sessionInfoHash[paper.session]; });
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makePaperRows(papers[0].start, papers[0].end, titles, sessions));
                    prevDay = sessionDay;
                }
            }

            /* append the output to the hidden table */
            $('#hidden-program-table tbody').append(output);
        }

        $(document).ready(function() {
            
            /* all the Remove All buttons are disabled on startup */
            $('.session-deselector').addClass('disabled');

            /* the include plenary checkbox is checked on startup */
            $('input#includePlenaryCheckBox').prop('checked', true);

            /* show the help window whenever "?" is pressed */
            $(document).keypress(function(event) {
                if (doWhichKey(event) == 63 && !helpShown) {
                    helpShown = true;
                    alertify.alert(instructions, function(event) { helpShown = false;});
                }
            });

            /* show the help window when the help button is clicked */
            $('a#help-button').on('click', function (event) {
                if (!helpShown) {
                    event.preventDefault();
                    helpShown = true;
                    alertify.alert(instructions, function(event) { helpShown = false;});
                }
            });

            /* expand/collapse all sessions when the toggle button is clicked */
            $('a#toggle-all-button').on('click', function (event) {
                event.preventDefault();
                var buttonText = $(this).text();

                / * expand all collapsed sessions */
                if (buttonText == 'Expand All Sessions ↓') {
                    $('div#expander').not('.expanded').trigger('click');
                    $(this).text('Collapse All Sessions ↑');
                }
                /* collapse all expanded sessions */
                else {
                    $('div#expander.expanded').trigger('click');
                    $(this).text('Expand All Sessions ↓');
                }
            });


            $('span.session-location, span.inline-location').on('click', function(event) {
                event.stopPropagation();
            });

            $('span.session-external-location').on('click', function(event) {
                var placeName = $(this).text().trim().replace(" ", "+");
                window.open("https://www.google.com/maps?q=" + placeName, "_blank");
                event.stopPropagation();
            });

            /* show the floorplan when any location is clicked */
            $('span.session-location, span.inline-location').magnificPopup({
                items: {
                    src: '/assets/images/square/square-3d-floor-plan.png'
                },
                type: 'image',
                fixedContentPos: 'auto'
            });

            /* get all the tutorial sessions and save the day and location for each of them in a hash */
            $('.session-tutorials').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.day = $(this).prevAll('.day:first').text().trim();
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* get all the workshop sessions and save the day and location for each of them in a hash */
            $('.session-workshops').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.day = $(this).prevAll('.day:first').text().trim();
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* get all the poster sessions and save the day and location for each of them in a hash */
            $('.session-posters').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.day = $(this).parent().prevAll('.day:first').text().trim();
                session.location = $(this).children('span.session-location').text().trim();
                var sessionTimeText = $(this).children('span.session-time').text().trim();                
                var sessionTimes = sessionTimeText.match(/\d+:\d+/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* get all the paper sessions and save the day and location for each of them in a hash */
            var paperSessions = $("[id|='session']").filter(function() { 
                return this.id.match(/session-\d\d?[a-z]$/);
            });
            $(paperSessions).each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.location = $(this).children('span.session-location').text().trim();
                session.day = $(this).parent().prevAll('.day:first').text().trim();
                var sessionTimeText = $(this).children('span.session-time').text().trim();                
                var sessionTimes = sessionTimeText.match(/\d+:\d+/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* iterate over all the papers and store all their info in a hash since we need that info whenever we click and hover and lookups will be faster than re-computing the info at each event */
            $('tr#paper').each(function() {
                var paperID = $(this).attr('paper-id');

                /* get the paper session and day */
                var paperSession = $(this).parents('.session');
                var sessionDay = paperSession.parent().prevAll('.day:first').text().trim();

                /* get the paper time and title */
                var paperTimeObj = $(this).children('#paper-time');
                var paperTitle = paperTimeObj.siblings('td').text().trim().replace(/\s\s+/g, " ");

                /* get the paper slot and the starting and ending times */
                var paperTimeText = paperTimeObj.text().trim();
                var paperTimes = paperTimeText.split('\u2013');
                var paperSlotStart = paperTimes[0];
                var paperSlotEnd = paperTimes[1];
                var exactPaperStartingTime = sessionDay + ' ' + paperSlotStart;
                var exactPaperEndingTime = sessionDay + ' ' + paperSlotEnd;

                paperInfoHash[paperID] = [new Date(exactPaperStartingTime).getTime(), new Date(exactPaperEndingTime).getTime(), paperSlotStart, paperSlotEnd, paperTitle, paperSession.attr('id')];
            });

            /* also save the plenary session info in another hash since we may need to add this to the pdf. Use the exact starting time as the hash key */
             $('.session-plenary').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                if (session.title == "Social Event") {
                    session.location = $(this).children('span.session-external-location').text().trim();
                }
                else {
                    session.location = $(this).children('span.session-location').text().trim();                    
                }
                session.day = $(this).prevAll('.day:first').text().trim();
                session.id = $(this).attr('id');
                var sessionTimeText = $(this).children('span.session-time').text().trim();
                var sessionTimes = sessionTimeText.match(/\d+:\d+/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                var exactSessionStartingTime = session.day + ' ' + sessionStart;
                plenarySessionHash[new Date(exactSessionStartingTime).getTime()] = session;
             });

            $('body').on('click', 'a.session-selector', function(event) {

                /* if we are disabled, do nothing */
                if ($(this).hasClass('disabled')) {
                    return false;
                }

                /* if we are choosing the entire session, then basically "click" on all of the not-selected papers */
                var sessionPapers = $(this).siblings('table.paper-table').find('tr#paper');
                var unselectedPapers = sessionPapers.not('.selected');
                unselectedPapers.trigger('click', true);

                /* now find out how many papers are selected after the trigger */
                var selectedPapers = sessionPapers.filter('.selected');

                /* disable myself (the choose all button) */
                $(this).addClass('disabled');

                /* if we didn't have any papers selected earlier, then enable the remove all button */
                if (unselectedPapers.length == sessionPapers.length) {
                    $(this).siblings('.session-deselector').removeClass('disabled');
                }

                /* this is not really a link */
                event.preventDefault();
                return false;
            });

            $('body').on('click', 'a.session-deselector', function(event) {

                /* if we are disabled, do nothing */
                if ($(this).hasClass('disabled')) {
                    return false;
                }

                /* otherwise, if we are removing the entire session, then basically "click" on all of the already selected papers */
                var sessionPapers = $(this).siblings('table.paper-table').find('tr#paper');
                var selectedPapers = sessionPapers.filter('.selected');
                selectedPapers.trigger('click', true);

                /* disable myself (the remove all button) */
                $(this).addClass('disabled');

                /* enable the choose all button */
                $(this).siblings('session-deselector').removeClass('disabled');

                /* if all the papers were selected earlier, then enable the choose all button */
                if (selectedPapers.length == sessionPapers.length) {
                    $(this).siblings('.session-selector').removeClass('disabled');                    
                }

                /* this is not really a link */
                event.preventDefault();
                return false;
            });

            /* hide all of the session details when starting up */
            $('[class$="-details"]').hide();

            /* expand sessions when their title is clicked */
            $('body').on('click', 'div.session-expandable .session-title, div#expander', function(event) {
                event.preventDefault();
                event.stopPropagation();
                var sessionObj = $(this).parent();

                /* if we had the shift key pressed, then expand ALL unexpanded parallel sessions including myself (only for papers) */
                if (event.shiftKey && sessionObj.attr('class').match('session-papers')) {
                    var sessionId = $(sessionObj).attr('id').match(/session-\d/)[0];
                    var parallelSessions = $(sessionObj).siblings().addBack().filter(function() { return this.id.match(sessionId); });

                    var unexpandedParallelSessions = $(parallelSessions).filter(function() { return !$(this).children('#expander').hasClass('expanded'); });

                    /* if all sessions are already expanded, then shift-clicking should close all of them */
                    if (unexpandedParallelSessions.length == 0) {
                        $.map(parallelSessions, closeSession);
                    }
                    else {
                        $.map(unexpandedParallelSessions, openSession);
                    }
                } 
                /* for a regular click, just toggle the individual session */
                else {
                    toggleSession(sessionObj);
                }
            });

            /* when we mouse over a paper icon, do not do anything */
            $('body').on('mouseover', 'table.paper-table tr#paper i[class$="-icon"]', function(event) {
                return false;
            });

            /* when we mouse over a paper, highlight the conflicting papers */
            $('body').on('mouseover', 'table.paper-table tr#paper', function(event) {
                var conflictingPapers = getConflicts($(this));
                $(this).addClass('hovered');
                $(conflictingPapers).addClass('conflicted');
            });

            /* when we mouse out, remove all highlights */
            $('body').on('mouseout', 'table.paper-table tr#paper', function(event) {
                var conflictingPapers = getConflicts($(this));
                $(this).removeClass('hovered');
                $(conflictingPapers).removeClass('conflicted');

            });

            $('body').on('click', 'a.info-button', function(event) {
                return false;
            });

            $('body').on('click', 'a.info-link', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'div.session-abstract', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'table.paper-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'table.tutorial-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'table.poster-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'div.paper-session-details', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'input#includePlenaryCheckBox', function(event) {
                    includePlenaryInSchedule = $(this).prop('checked');
            });

            $('body').on('click', 'a#generatePDFButton', function(event) {
                /* if we haven't chosen any papers, and we aren't including plenary sessions either, then raise an error. If we are including plenary sessions and no papers, then confirm. */
                event.preventDefault();
                var numChosenItems = Object.keys(chosenPapersHash).length + Object.keys(chosenTutorialsHash).length + Object.keys(chosenWorkshopsHash).length + Object.keys(chosenPostersHash).length;
                if (numChosenItems == 0) {
                    if (includePlenaryInSchedule) {
                        alertify.confirm("The PDF will contain only the plenary sessions since nothing was chosen. Proceed?", function () { generatePDFfromTable();
                                }, function() { return false; });
                    }
                    else {
                        alertify.alert('Nothing to generate. Nothing was chosen and plenary sessions were excluded.');
                        return false;
                    }
                }
                else {
                    generatePDFfromTable();
                }
            });

            $('body').on('click', 'table.tutorial-table tr#tutorial', function(event) {
                event.preventDefault();
                var tutorialTimeObj = $(this).parents('.session-tutorials').children('.session-time');
                var tutorialInfo = getTutorialInfoFromTime(tutorialTimeObj);
                var tutorialObject = {};
                var exactStartingTime = tutorialInfo[0];
                tutorialObject.start = tutorialInfo[1];
                tutorialObject.end = tutorialInfo[2];
                tutorialObject.title = $(this).find('.tutorial-title').text();
                tutorialObject.session = tutorialInfo[3];
                tutorialObject.location = $(this).find('.inline-location').text();
                tutorialObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected tutorial */
                if (isChosen(exactStartingTime, tutorialObject, 'tutorial')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, tutorialObject, 'tutorial');
                }
                else {
                    addToChosen(exactStartingTime, tutorialObject, 'tutorial');
                    $(this).addClass('selected');                    
                }
            });

            $('body').on('click', 'table.workshop-table tr#workshop', function(event) {
                event.preventDefault();
                var workshopTimeObj = $(this).parents('.session-workshops').children('.session-time');
                var workshopInfo = getWorkshopInfoFromTime(workshopTimeObj);
                var workshopObject = {};
                var exactStartingTime = workshopInfo[0];
                workshopObject.start = workshopInfo[1];
                workshopObject.end = workshopInfo[2];
                workshopObject.title = $(this).find('.workshop-title').text();
                workshopObject.session = workshopInfo[3];
                workshopObject.location = $(this).find('.inline-location').text();
                workshopObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected workshop */
                if (isChosen(exactStartingTime, workshopObject, 'workshop')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, workshopObject, 'workshop');
                }
                else {
                    addToChosen(exactStartingTime, workshopObject, 'workshop');
                    $(this).addClass('selected');                    
                }
            });

            $('body').on('click', 'table.poster-table tr#poster', function(event) {
                event.preventDefault();
                var posterTimeObj = $(this).parents('.session-posters').children('.session-time');
                var posterInfo = getPosterInfoFromTime(posterTimeObj);
                var posterObject = {};
                var exactStartingTime = posterInfo[0];
                posterObject.start = posterInfo[1];
                posterObject.end = posterInfo[2];
                posterObject.title = $(this).find('.poster-title').text().trim();
                posterObject.type = $(this).parents('.poster-table').prevAll('.poster-type:first').text().trim();
                posterObject.session = posterInfo[3];
                posterObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected poster */
                if (isChosen(exactStartingTime, posterObject, 'poster')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, posterObject, 'poster');
                }
                else {
                    addToChosen(exactStartingTime, posterObject, 'poster');
                    $(this).addClass('selected');
                    var key = new Date(exactStartingTime).getTime();
                    if (key in plenarySessionHash) {
                        delete plenarySessionHash[key];
                    }
                }
            });

            /* open the URL in a new window/tab when we click on the any icon - whether it is the keynote slides or the video */            
            $('body').on('click', 'div.session-abstract p i[class$="-icon"]', function(event) {
                event.stopPropagation();
                event.preventDefault();
                var urlToOpen = $(this).attr('data');
                if (urlToOpen !== '') {
                    window.open(urlToOpen, "_blank");
                }
            });


            /* open the anthology or video URL in a new window/tab when we click on the PDF or video icon respectively  */            
            $('body').on('click', 'table.tutorial-table tr#tutorial i[class$="-icon"],table.paper-table tr#paper i[class$="-icon"],table.paper-table tr#best-paper i[class$="-icon"],table.poster-table tr#poster i[class$="-icon"]', function(event) {
                event.stopPropagation();
                event.preventDefault();
                var urlToOpen = $(this).attr('data');
                if (urlToOpen !== '') {
                    window.open(urlToOpen, "_blank");
                }
            });

            $('body').on('click', 'table.paper-table tr#paper', function(event, fromSession) {
                event.preventDefault();
                $(this).removeClass('hovered');
                getConflicts($(this)).removeClass('conflicted');
                var paperID = $(this).attr('paper-id');
                var paperTimeObj = $(this).children('td#paper-time');
                var paperInfo = paperInfoHash[paperID];
                var paperObject = {};
                var exactStartingTime = paperInfo[0];
                paperObject.start = paperInfo[2];
                paperObject.end = paperInfo[3];
                paperObject.title = paperInfo[4];
                paperObject.session = paperInfo[5];
                paperObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected paper */
                if (isChosen(exactStartingTime, paperObject, 'paper')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, paperObject, 'paper');

                    /* if we are not being triggered at the session level, then we need to handle the state of the session level button ourselves */
                    if (!fromSession) {
        
                        /* we also need to enable the choose button */
                        $(this).parents('table.paper-table').siblings('.session-selector').removeClass('disabled');

                        /* we also need to disable the remove button if this was the only paper selected in the session */
                        var selectedPapers = $(this).siblings('tr#paper').filter('.selected');
                        if (selectedPapers.length == 0) {
                            $(this).parents('table.paper-table').siblings('.session-deselector').addClass('disabled');
                        }
                    }
                }
                else {
                    /* if we are selecting a previously unselected paper */
                    addToChosen(exactStartingTime, paperObject, 'paper');
                    $(this).addClass('selected');

                    /* if we are not being triggered at the session level, then we need to handle the state of the session level button ourselves */
                    if (!fromSession) {

                        /* we also need to enable the remove button */
                        $(this).parents('table.paper-table').siblings('.session-deselector').removeClass('disabled');

                        /* and disable the choose button if all the papers are now selected anyway */
                        var sessionPapers = $(this).siblings('tr#paper');
                        var selectedPapers = sessionPapers.filter('.selected');
                        if (sessionPapers.length == selectedPapers.length) {
                            $(this).parents('table.paper-table').siblings('.session-selector').addClass('disabled');
                        }
                    }
                }
            });
        });
    </script>
---
{% include base_path %}
<link rel="stylesheet" href="assets/css/alertify.css" id="alertifyCSS">

<table id="hidden-program-table">
    <thead>
        <tr><th>time</th><th>location</th><th>info</th></tr>
    </thead>
    <tbody></tbody>
</table>

<div id="introParagraph">
        <p>On this page, you can choose the sessions (and individual papers/posters) of your choice <em>and</em> generate a PDF of your customized schedule! This page should work on modern browsers on all operating systems. On mobile devices, Safari on iOS and Chrome on Android are the only browsers known to work. For the best experience, use a non-mobile device. For help, simply type "?"" while on the page or click on the "Help" button.</p>
</div>

<p class="text-center">
    <a href="#" id="help-button" class="btn btn--small btn--info">Help</a>
</p>
<p class="text-center">
    <a href="#" id="toggle-all-button" class="btn btn--small btn--info">Expand All Sessions ↓</a>
</p>

<div class="schedule">




<!-- TUTORIAL AND WORKSHOP SCHEDULE --> 


<div class="day" id="first-day">Sunday, 3 November 2019</div>

	<!-- MORNING TUTORIALS -->
	<div class="session session-expandable session-tutorials" id="session-morning-tutorials1">
        <div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/>
        <span class="session-time" title="Sunday, November 3 2019">09:00 &ndash; 12:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">
                        	<strong>[T1] Dive into Deep Learning for Natural Language Processing.</strong> 
                        	Haibin Lin, Xingjian Shi, Leonard Lausen, Aston Zhang, He He, Sheng Zha and Alexander Smola.
                        </span>
                        <br/>
                        <span class="btn btn--info btn--location inline-location">
                        	TBA
                        </span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">
                        	<strong>[T2] Processing and Understanding Mixed Language Data.</strong> 
                        	Monojit Choudhury and Kalika Bali.
                        </span>
                        <br/>
                        <span class="btn btn--info btn--location inline-location">
                        	TBA
                        </span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    
    <!-- LUNCH BREAK -->
    <div class="session session-break session-plenary" id="session-lunch-1">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time" title="Sunday, November 3 2019">12:30 &ndash; 14:00</span>
    </div>    
    
    <!-- AFTERNOON TUTORIALS -->
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials1">
        <div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/>
        <span class="session-time" title="Sunday, November 3 2019">14:00 &ndash; 17:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
            	<tr id="tutorial">
                    <td>
                        <span class="tutorial-title">
                        	<strong>[T1] Dive into Deep Learning for Natural Language Processing  (cont.).</strong> 
                        	Haibin Lin, Xingjian Shi, Leonard Lausen, Aston Zhang, He He, Sheng Zha and Alexander Smola.
                        </span>
                        <br/>
                        <span class="btn btn--info btn--location inline-location">
                        	TBA
                        </span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">
                        	<strong>[T3] Data Collection and End-to-End Learning for Conversational AI.</strong> 
                        	Tsung-Hsien Wen, Pei-Hao Su, Pawe&#322; Budzianowski, I&ntilde;igo Casanueva and Ivan Vuli&#263;.
                        </span>
                        <br/>
                        <span class="btn btn--info btn--location inline-location">
                        	TBA
                        </span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    
    <!-- WORKSHOPS -->
    <div class="session session-expandable session-workshops" id="session-workshops-1">
        <div id="expander"></div><a href="#" class="session-title">Workshops &amp; Co-located Events</a><br/>
        <span class="session-time" title="Sunday, November 3 2019">08:30 &ndash; 18:00</span><br/>
        <div class="workshop-session-details">
            <br/>
            <table class="workshop-table">
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W1] CoNLL 2019: The Conference on Computational Natural Language Learning (Day 1).</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W2] FEVER: The second workshop on Fact Extraction and VERification.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W3] DiscoMT19: Discourse in Machine Translation 2019 (half day).</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W4] LANTERN: Beyond Vision and Language: Integrating Knowledge from the Real World (half day).</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W5] MSR 2019: The second Workshop on Multilingual Surface Realization.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W6] LOUHI 2019: The Tenth International Workshop on Health Text Mining and Information Analysis.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W7] DeepLo 2019: Deep Learning for Low-Resource Natural Language Processing.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W8] COIN: COmmonsense INference in NLP.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W9] AnnoNLP: Aggregating and analysing crowdsourced annotations for NLP.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    
    
<!-- SECOND TUTORIAL AND WORKSHOP DAY -->
<div class="day" id="second-day">Monday, 4 November 2019</div>
    
	<!-- MORNING TUTORIALS -->  	  
    <div class="session session-expandable session-tutorials" id="session-morning-tutorials2">
        <div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/>
        <span class="session-time" title="Monday November 4 2019">09:00 &ndash; 12:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">
                        	<strong>[T4] Bias and Fairness in Natural Language Processing.</strong> 
                        	Kai-Wei Chang, Margaret Mitchell and Vicente Ordonez.
                        </span>
                        <br/>
                        <span class="btn btn--info btn--location inline-location">
                        	TBA
                        </span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">
                        	<strong>[T5] Discreteness in Neural Natural Language Processing.</strong> 
                        	Lili Mou, Hao Zhou and Lei Li.
                        </span>
                        <br/>
                        <span class="btn btn--info btn--location inline-location">
                        	TBA
                        </span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    
    <!-- LUNCH BREAK -->
    <div class="session session-break session-plenary" id="session-lunch-2">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time" title="Monday November 4 2019">12:30 &ndash; 14:00</span>
    </div>    
    
    <!-- AFTERNOON TUTORIALS -->
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials2">
        <div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/>
        <span class="session-time" title="Monday November 4 2019">14:00 &ndash; 17:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">
                        	<strong>[T6] Graph-based Deep Learning in Natural Language Processing.</strong> 
                        	Shikhar Vashishth, Naganand Yadati and Partha Talukdar.
                        </span>
                        <br/>
                        <span class="btn btn--info btn--location inline-location">
                        	TBA
                        </span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">
                        	<strong>[T7] Semantic Specialization of Distributional Word Vectors.</strong> 
                        	Goran Glava&#347;, Edoardo Maria Ponti and Ivan Vuli&#263;.
                        </span>
                        <br/>
                        <span class="btn btn--info btn--location inline-location">
                        	TBA
                        </span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    
    <!-- WORKSHOPS -->
    <div class="session session-expandable session-workshops" id="session-workshops-2">
        <div id="expander"></div><a href="#" class="session-title">Workshops &amp; Co-located Events</a><br/>
        <span class="session-time" title="Monday November 4 2019">09:00 &ndash; 17:00</span><br/>
        <div class="workshop-session-details">
            <br/>
            <table class="workshop-table">
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W1] CoNLL 2019: The Conference on Computational Natural Language Learning (Day 2).</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W10] MRQA: The 2nd Workshop on Machine Reading for Question Answering.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W11] BioNLP-OST 2019: International Workshop on BioNLP Open Shared Tasks 2019.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W12] WNGT: The 3rd Workshop on Neural Generation and Translation.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W13] W-NUT 2019: The 5th Workshop on Noisy User-generated Text.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W14] NewSum: The Workshop on New Frontiers in Summarization.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W15] TextGraphs-19: Graph-based Methods for Natural Language Processing.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W16] WAT2019: The 6th Workshop on Asian Translation.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W17] ECONLP 2019: The 2nd Workshop on Economics and Natural Language Processing.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
                <tr id="workshop">
                    <td>
                        <span class="workshop-title"><strong>[W18] NLP4IF: NLP for Freedom: Censorship, Disinformation, and Propaganda.</strong></span> 
                        <br/>
                        <span class="btn btn--info btn--location inline-location">TBA</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    
    <!-- WELCOME RECEPTION -->
    <div class="session session-expandable session-plenary" id="session-reception">
        <div id="expander"></div>
        <a href="#" class="session-title">Welcome Reception</a>
        <br/>
        <span class="session-time" title="Monday November 4 2019">18:00 &ndash; 20:00</span>
        <br/>
        <span class="session-location btn btn--info btn--location">AsiaWorld Summit (Hall 2) and East Concourse, AsiaWorld Expo</span>
        <div class="paper-session-details">
            <br/><br/>
            <div class="session-abstract">
                <p>Catch up with your colleagues at the Welcome Reception in the conference venue, AsiaWorld Expo.</p>
            </div>
		</div>
	</div>







<!-- MAIN CONFERENCE SCHEDULE -->

<div class="day" id="day-3">Tuesday, 5 November 2019</div>
<div class="session session-plenary" id="session-welcome"><span class="session-title">Opening Remarks</span><br/><span class="session-time" title="Tuesday, 5 November 2019">08:45 &ndash; 09:00</span><br/> <span class="session-location btn btn--info btn--location">Hall 2C</span></div>
<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>Keynote I: "Project Debater - how persuasive can a computer be?"</strong></a><br/><span class="session-people"><a href="http://researcher.watson.ibm.com/researcher/view.php?person=il-NOAMS" target="_blank">Noam Slonim (IBM Haifa Research Lab)</a></span><br/><span class="session-time" title="Tuesday, 5 November 2019">09:00 &ndash; 10:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><div class="paper-session-details"><br/><div class="session-abstract"><p>Project Debater is the first AI system that can meaningfully debate a human opponent. The system, an IBM Grand Challenge, is designed to build coherent, convincing speeches on its own, as well as provide rebuttals to the opponent’s main arguments. In February 2019, Project Debater competed against Harish Natarajan, who holds the world record for most debate victories, in an event held in San Francisco that was broadcasted live world-wide. In this talk I will tell the story of Project Debater, from conception to a climatic final event, describe its underlying technology, and discuss how it can be leveraged for advancing decision making and critical thinking.</p></div></div></div>
<div class="session session-break session-plenary" id="session-break-1"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Tuesday, 5 November 2019">10:00 &ndash; 10:30</span></div>
<div class="session-box" id="session-box-1"><div class="session-header" id="session-header-1"> (Session 1)</div>
<div class="session session-expandable session-papers1" id="session-1a"><div id="expander"></div><a href="#" class="session-title">1A: Machine Learning I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1443"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Attending to Future Tokens for Bidirectional Sequence Generation. </span><em>Carolin Lawrence, Bhushan Kotnis and Mathias Niepert</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1443" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="526"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Attention is not not Explanation. </span><em>Sarah Wiegreffe and Yuval Pinter</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-526" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1176"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Practical Obstacles to Deploying Active Learning. </span><em>David Lowell, Zachary C. Lipton and Byron C. Wallace</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1176" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1207"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Transfer Learning Between Related Tasks Using Expected Label Proportions. </span><em>Matan Ben Noach and Yoav Goldberg</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1207" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="TACL-1732"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Insertion-based Decoding with automatically Inferred Generation Order. </span><em>Jiatao Gu, Qi Liu and Kyunghyun Cho</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1732" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-1b"><div id="expander"></div><a href="#" class="session-title">1B: Lexical Semantics I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3403"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Knowledge Enhanced Contextual Word Representations. </span><em>Matthew E. Peters, Mark Neumann, Robert Logan, Roy Schwartz, Vidur Joshi, Sameer Singh and Noah A. Smith</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3403" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="208"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">How Contextual are Contextualized Word Representations? Comparing the Geometry of BERT, ELMo, and GPT-2 Embeddings. </span><em>Kawin Ethayarajh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-208" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="783"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Room to Glo: A Systematic Comparison of Semantic Change Detection Approaches with Word Embeddings. </span><em>Philippa Shoemark, Farhana Ferdousi Liza, Dong Nguyen, Scott Hale and Barbara McGillivray</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-783" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3976"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Correlations between Word Vector Sets. </span><em>Vitalii Zhelezniak, April Shen, Daniel Busbridge, Aleksandar Savkov and Nils Hammerla</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3976" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1724"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Game Theory Meets Embeddings: a Unified Framework for Word Sense Disambiguation. </span><em>Rocco Tripodi and Roberto Navigli</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1724" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-1c"><div id="expander"></div><a href="#" class="session-title">1C: Dialog &amp; Interactive Systems I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="166"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Guided Dialog Policy Learning: Reward Estimation for Multi-Domain Task-Oriented Dialog. </span><em>Ryuichi Takanobu, Hanlin Zhu and Minlie Huang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-166" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="554"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Multi-hop Selector Network for Multi-turn Response Selection in Retrieval-based Chatbots. </span><em>Chunyuan Yuan, Wei Zhou, Mingming Li, Shangwen Lv, Fuqing Zhu, Jizhong Han and Songlin Hu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-554" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1053"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">MoEL: Mixture of Empathetic Listeners. </span><em>Zhaojiang Lin, Andrea Madotto, Jamin Shin, Peng Xu and Pascale Fung</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1053" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2430"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Entity-Consistent End-to-end Task-Oriented Dialogue System with KB Retriever. </span><em>Libo Qin, Yijia Liu, Wanxiang Che, Haoyang Wen, Yangming Li and Ting Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2430" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3756"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Building Task-Oriented Visual Dialog Systems Through Alternative Optimization Between Dialog Policy and Language Generation. </span><em>Mingyang Zhou, Josh Arnold and Zhou Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3756" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-1d"><div id="expander"></div><a href="#" class="session-title">1D: Sentiment Analysis &amp; Argument Mining I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-1d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-1d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2092"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">DialogueGCN: A Graph Convolutional Neural Network for Emotion Recognition in Conversation. </span><em>Deepanway Ghosal, Navonil Majumder, Soujanya Poria, Niyati Chhaya and Alexander Gelbukh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2092" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1814"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Knowledge-Enriched Transformer for Emotion Detection in Textual Conversations. </span><em>Peixiang Zhong, Di Wang and Chunyan Miao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1814" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3544"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Interpretable Relevant Emotion Ranking with Event-Driven Attention. </span><em>Yang Yang, Deyu ZHOU, Yulan He and Meng Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3544" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="518"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Justifying Recommendations using Distantly-Labeled Reviews and Fine-Grained Aspects. </span><em>Jianmo Ni, Jiacheng Li and Julian McAuley</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-518" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="204"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Using Customer Service Dialogues for Satisfaction Analysis with Context-Assisted Multiple Instance Learning. </span><em>Kaisong Song, Lidong Bing, Wei Gao, Jun Lin, Lujun Zhao, Jiancheng Wang, Changlong Sun, Xiaozhong Liu and Qiong Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-204" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-1"><div id="expander"></div><a href="#" class="session-title">1 Poster & Demo: Information Extraction, Information Retrieval &amp; Document Analysis, Linguistic Theories </a><br/><span class="session-time" title="Tuesday, 5 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="249"><td><span class="poster-title">Leveraging Dependency Forest for Neural Medical Relation Extraction. </span><em>Linfeng Song, Yue Zhang, Daniel Gildea, Mo Yu, Zhiguo Wang and jinsong su</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-249" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="569"><td><span class="poster-title">Open Relation Extraction: Relational Knowledge Transfer from Supervised Data to Unsupervised Data. </span><em>Ruidong Wu, Yuan Yao, Xu Han, Ruobing Xie, Zhiyuan Liu, Fen Lin, Leyu Lin and Maosong Sun</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-569" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="710"><td><span class="poster-title">Improving Relation Extraction with Knowledge-attention. </span><em>Pengfei Li, Kezhi Mao, Xuefeng Yang and Qi Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-710" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="782"><td><span class="poster-title">Jointly Learning Entity and Relation Representations for Entity Alignment. </span><em>Yuting Wu, Xiao Liu, Yansong Feng, Zheng Wang and Dongyan Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-782" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="796"><td><span class="poster-title">Tackling Long-Tailed Relations and Uncommon Entities in Knowledge Graph Completion. </span><em>Zihao Wang, Kwunping Lai, Piji Li, Lidong Bing and Wai Lam</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-796" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="821"><td><span class="poster-title">Low-Resource Name Tagging Learned with Weakly Labeled Data. </span><em>Yixin Cao, Zikun Hu, Tat-seng Chua, Zhiyuan Liu and Heng Ji</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-821" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="841"><td><span class="poster-title">Learning Dynamic Context Augmentation for Global Entity Linking. </span><em>Xiyuan Yang, Xiaotao Gu, Sheng Lin, Siliang Tang, Yueting Zhuang, Fei Wu, Zhigang Chen, Guoping Hu and Xiang Ren</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-841" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="859"><td><span class="poster-title">Open Event Extraction from Online Text using a Generative Adversarial Network. </span><em>Rui Wang, Deyu ZHOU and Yulan He</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-859" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1001"><td><span class="poster-title">Learning to Bootstrap for Entity Set Expansion. </span><em>Lingyong Yan, Xianpei Han, Le Sun and Ben He</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1001" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1149"><td><span class="poster-title">Multi-Input Multi-Output Sequence Labeling for Joint Extraction of Fact and Condition Tuples from Scientific Text. </span><em>Tianwen Jiang, Tong Zhao, Bing Qin, Ting Liu, Nitesh Chawla and Meng Jiang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1149" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1210"><td><span class="poster-title">Cross-lingual Structure Transfer for Relation and Event Extraction. </span><em>Ananya Subburathinam, Di Lu, Heng Ji, Jonathan May, Shih-Fu Chang, Avirup Sil and Clare Voss</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1210" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1365"><td><span class="poster-title">Uncover the Ground-Truth Relations in Distant Supervision: A Neural Expectation-Maximization Framework. </span><em>Junfan Chen, Richong Zhang, Yongyi Mao, Hongyu Guo and Jie Xu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1365" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1736"><td><span class="poster-title">Doc2EDAG: An End-to-End Document-level Framework for Chinese Financial Event Extraction. </span><em>Shun Zheng, Wei Cao, Wei Xu and Jiang Bian</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1736" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1816"><td><span class="poster-title">Event Detection with Trigger-Aware Lattice Neural Network. </span><em>Ning Ding, Ziran Li, Zhiyuan Liu, Haitao Zheng and Zibo Lin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1816" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1874"><td><span class="poster-title">A Boundary-aware Neural Model for Nested Named Entity Recognition. </span><em>Changmeng Zheng, Yi Cai, Jingyun Xu, Ho-fung Leung and Guandong Xu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1874" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2024"><td><span class="poster-title">Learning the Extraction Order of Multiple Relational Facts in a Sentence with Reinforcement Learning. </span><em>Xiangrong Zeng, Shizhu He, Daojian Zeng, Kang Liu, Shengping Liu and Jun Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2024" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2439"><td><span class="poster-title">CaRe: Open Knowledge Graph Embeddings. </span><em>Swapnil Gupta, Sreyash Kenkre and Partha Talukdar</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2439" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2793"><td><span class="poster-title">Self-Attention Enhanced CNNs and Collaborative Curriculum Learning for Distantly Supervised Relation Extraction. </span><em>Yuyun Huang and Jinhua Du</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2793" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3014"><td><span class="poster-title">Neural Cross-Lingual Relation Extraction Based on Bilingual Word Embedding Mapping. </span><em>Jian Ni and Radu Florian</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3014" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3059"><td><span class="poster-title">Leveraging 2-hop Distant Supervision from Table Entity Pairs for Relation Extraction. </span><em>xiang deng and Huan Sun</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3059" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3317"><td><span class="poster-title">EntEval: A Holistic Evaluation Benchmark for Entity Representations. </span><em>Mingda Chen, Zewei Chu, Yang Chen, Karl Stratos and Kevin Gimpel</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3317" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3646"><td><span class="poster-title">Joint Event and Temporal Relation Extraction with Shared Representations and Structured Prediction. </span><em>Rujun Han, Qiang Ning and Nanyun Peng</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3646" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="32"><td><span class="poster-title">Hierarchical Text Classification with Reinforced Label Assignment. </span><em>Yuning Mao, Jingjing Tian, Jiawei Han and Xiang Ren</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-32" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="314"><td><span class="poster-title">Investigating Capsule Network and Semantic Feature on Hyperplanes for Text Classification. </span><em>Chunning Du, Haifeng Sun, Jingyu Wang, Qi Qi, Jianxin Liao, Chun Wang and Bing Ma</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-314" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="721"><td><span class="poster-title">Label-Specific Document Representation for Multi-Label Text Classification. </span><em>Lin Xiao, Xin Huang, Boli Chen and Liping Jing</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-721" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="729"><td><span class="poster-title">Hierarchical Attention Prototypical Networks for Few-Shot Text Classification. </span><em>Shengli Sun, Qingfeng Sun, Kevin Zhou and Tengchao Lv</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-729" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2087"><td><span class="poster-title">Many Faces of Feature Importance: Comparing Built-in and Post-hoc Feature Importance in Text Classification. </span><em>Vivian Lai, Zheng Cai and Chenhao Tan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2087" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2273"><td><span class="poster-title">Enhancing Local Feature Extraction with Global Representation for Neural Text Classification. </span><em>Guocheng Niu, Hengru Xu, Bolei He, Xinyan Xiao, Hua Wu and Sheng GAO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2273" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3004"><td><span class="poster-title">Latent-Variable Generative Models for Data-Efficient Text Classification. </span><em>Xiaoan Ding and Kevin Gimpel</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3004" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3239"><td><span class="poster-title">PaRe: A Paper-Reviewer Matching Approach Using a Common Topic Space. </span><em>Omer Anjum, Hongyu Gong, Suma Bhat, Wen-Mei Hwu and JinJun Xiong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3239" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2750"><td><span class="poster-title">Linking artificial and human neural representations of language. </span><em>Jon Gauthier and Roger Levy</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2750" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-30"><td><span class="poster-title">IFlyLegal: A Chinese Legal System for Consultation, Law Searching, and Document Analysis. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-30" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-47"><td><span class="poster-title">TellMeWhy: Learning to Explain Corrective Feedback for Second Language Learners. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-47" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-50"><td><span class="poster-title">Honkling: In-Browser Personalization for Ubiquitous Keyword Spotting. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-50" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-64"><td><span class="poster-title">Redcoat: A Collaborative Annotation Tool for Hierarchical Entity Typing. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-64" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-78"><td><span class="poster-title">SEAGLE: A Platform for Comparative Evaluation of Semantic Encoders for Information Retrieval. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-78" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-80"><td><span class="poster-title">OpenNRE: An Open and Extensible Toolkit for Neural Relation Extraction. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-80" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-81"><td><span class="poster-title">Automatic Taxonomy Induction and Expansion. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-81" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-87"><td><span class="poster-title">Applying BERT to Document Retrieval with Birch. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-87" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-lunch-3"><span class="session-title">Lunch</span><br/><span class="session-time" title="Tuesday, 5 November 2019">12:00 &ndash; 13:30</span></div>
<div class="session-box" id="session-box-2"><div class="session-header" id="session-header-2"> (Session 2)</div>
<div class="session session-expandable session-papers1" id="session-2a"><div id="expander"></div><a href="#" class="session-title">2A: Summarization &amp; Generation</a><br/><span class="session-time" title="Tuesday, 5 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3687"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Neural Text Summarization: A Critical Evaluation. </span><em>Wojciech Kryscinski, Nitish Shirish Keskar, Bryan McCann, Caiming Xiong and Richard Socher</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3687" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2586"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Neural data-to-text generation: A comparison between pipeline and end-to-end architectures. </span><em>Thiago Castro Ferreira, Chris van der Lee, Emiel van Miltenburg and Emiel Krahmer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2586" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1175"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">MoverScore: Text Generation Evaluating with Contextualized Embeddings and Earth Mover Distance. </span><em>Wei Zhao, Maxime Peyrard, Fei Liu, Yang Gao, Christian M. Meyer and Steffen Eger</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1175" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3049"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Select and Attend: Towards Controllable Content Selection in Text Generation. </span><em>Xiaoyu Shen, Jun Suzuki, Kentaro Inui, Hui Su, Dietrich Klakow and Satoshi Sekine</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3049" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3357"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Sentence-Level Content Planning and Style Specification for Neural Text Generation. </span><em>Xinyu Hua and Lu Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3357" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-2b"><div id="expander"></div><a href="#" class="session-title">2B: Sentence-level Semantics I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2740"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Translate and Label! An Encoder-Decoder Approach for Cross-lingual Semantic Role Labeling. </span><em>Angel Daza and Anette Frank</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2740" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2106"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Syntax-Enhanced Self-Attention-Based Semantic Role Labeling. </span><em>Yue Zhang, Rui Wang and Luo Si</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2106" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2213"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">VerbAtlas: a Novel Large-Scale Verbal Semantic Resource and Its Application to Semantic Role Labeling. </span><em>Andrea Di Fabio, Simone Conia and Roberto Navigli</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2213" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1099"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Parameter-free Sentence Embedding via Orthogonal Basis. </span><em>Ziyi Yang, Chenguang Zhu and Weizhu Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1099" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3807"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Evaluation Benchmarks and Learning Criteria for Discourse-Aware Sentence Representations. </span><em>Mingda Chen, Zewei Chu and Kevin Gimpel</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3807" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-2c"><div id="expander"></div><a href="#" class="session-title">2C: Speech, Vision, Robotics, Multimodal &amp; Grounding I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3013"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Extracting Possessions from Social Media: Images Complement Language. </span><em>Dhivya Chinnappa, Srikala Murugan and Eduardo Blanco</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3013" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1243"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Learning to Speak and Act in a Fantasy Text Adventure Game. </span><em>Jack Urbanek, Angela Fan, Siddharth Karamcheti, Saachi Jain, Samuel Humeau, Emily Dinan, Tim Rocktäschel, Douwe Kiela, Arthur Szlam and Jason Weston</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1243" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1542"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Help, Anna! Visual Navigation with Natural Multimodal Assistance via Retrospective Curiosity-Encouraging Imitation Learning. </span><em>Khanh Nguyen and Hal Daumé III</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1542" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2247"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Incorporating Visual Semantics into Sentence Representations within a Grounded Space. </span><em>Patrick Bordes, Eloi Zablocki, Laure Soulier, Benjamin Piwowarski and patrick Gallinari</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2247" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3024"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Neural Naturalist: Generating Fine-Grained Image Comparisons. </span><em>Maxwell Forbes, Christine Kaeser-Chen, Piyush Sharma and Serge Belongie</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3024" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-2d"><div id="expander"></div><a href="#" class="session-title">2D: Information Extraction I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-2d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-2d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="116"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Fine-Grained Evaluation for Entity Linking. </span><em>Henry Rosales-Méndez, Aidan Hogan and Barbara Poblete</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-116" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3069"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Supervising Unsupervised Open Information Extraction Models. </span><em>Arpita Roy, Youngja Park, Taesung Lee and Shimei Pan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3069" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1723"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Neural Cross-Lingual Event Detection with Minimal Parallel Resources. </span><em>Jian Liu, Yubo Chen, Kang Liu and Jun Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1723" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1258"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">KnowledgeNet: A Benchmark Dataset for Knowledge Base Population. </span><em>Filipe Mesquita, Matteo Cannaviccio, Jordan Schmidek, Paramita Mirza and Denilson Barbosa</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1258" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3308"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Effective Use of Transformer Networks for Entity Tracking. </span><em>Aditya Gupta and Greg Durrett</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3308" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-2"><div id="expander"></div><a href="#" class="session-title">2 Poster & Demo: Machine Translation &amp; Mulitilinguality, Phonology, Morphology &amp; Word Segmentation, Tagging, Chunking, Syntax &amp; Parsing </a><br/><span class="session-time" title="Tuesday, 5 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="233"><td><span class="poster-title">Explicit Cross-lingual Pre-training for Unsupervised Machine Translation. </span><em>Shuo Ren, Yu Wu, Shujie Liu, Ming Zhou and Shuai Ma</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-233" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="410"><td><span class="poster-title">Latent Part-of-Speech Sequences for Neural Machine Translation. </span><em>Xuewen Yang, Yingru Liu, Dongliang Xie, Xin Wang and Niranjan Balasubramanian</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-410" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="798"><td><span class="poster-title">Improving Back-Translation with Uncertainty-based Confidence Estimation. </span><em>Shuo Wang, Yang Liu, Chao Wang, Huanbo Luan and Maosong Sun</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-798" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="846"><td><span class="poster-title">Towards Linear Time Neural Machine Translation with Capsule Networks. </span><em>Mingxuan Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-846" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="985"><td><span class="poster-title">Modeling Multi-mapping Relations for Precise Cross-lingual Entity Alignment. </span><em>Xiaofei Shi and Yanghua Xiao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-985" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1226"><td><span class="poster-title">Supervised and Nonlinear Alignment of Two Embedding Spaces for Dictionary Induction in Low Resourced Languages. </span><em>Masud Moshtaghi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1226" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1414"><td><span class="poster-title">Beto, Bentz, Becas: The Surprising Cross-Lingual Effectiveness of BERT. </span><em>Shijie Wu and Mark Dredze</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1414" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1427"><td><span class="poster-title">Iterative Dual Domain Adaptation for Neural Machine Translation. </span><em>Jiali Zeng, Yang Liu, jinsong su, yubing Ge, Yaojie Lu, Yongjing Yin and jiebo luo</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1427" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1484"><td><span class="poster-title">Multi-agent Learning for Neural Machine Translation. </span><em>tianchi bi, hao xiong, Zhongjun He, Hua Wu and Haifeng Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1484" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1869"><td><span class="poster-title">Pivot-based Transfer Learning for Neural Machine Translation between Non-English Languages. </span><em>Yunsu Kim, Petre Petrov, Pavel Petrushkov, Shahram Khadivi and Hermann Ney</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1869" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1967"><td><span class="poster-title">Context-Aware Monolingual Repair for Neural Machine Translation. </span><em>Elena Voita, Rico Sennrich and Ivan Titov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1967" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2330"><td><span class="poster-title">Multi-Granularity Self-Attention for Neural Machine Translation. </span><em>Jie Hao, Xing Wang, Shuming Shi, Jinfeng Zhang and Zhaopeng Tu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2330" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2537"><td><span class="poster-title">Improving Deep Transformer with Depth-Scaled Initialization and Merged Attention. </span><em>Biao Zhang, Ivan Titov and Rico Sennrich</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2537" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2961"><td><span class="poster-title">A Discriminative Neural Model for Cross-Lingual Word Alignment. </span><em>Elias Stengel-Eskin, Tzu-ray Su, Matt Post and Benjamin Van Durme</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2961" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3571"><td><span class="poster-title">One Model to Learn Both: Zero Pronoun Prediction and Translation. </span><em>Longyue Wang, Zhaopeng Tu, Xing Wang and Shuming Shi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3571" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3601"><td><span class="poster-title">Dynamic Past and Future for Neural Machine Translation. </span><em>Zaixiang Zheng, Shujian Huang, Zhaopeng Tu, XIN-YU DAI and Jiajun CHEN</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3601" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3770"><td><span class="poster-title">Revisit Automatic Error Detection for Wrong and Missing Translation -- A Supervised Approach. </span><em>Wenqiang Lei, Weiwen Xu, Ai Ti Aw, Yuanxin Xiang and Tat Seng Chua</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3770" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3857"><td><span class="poster-title">Towards Understanding Neural Machine Translation with Word Importance. </span><em>Shilin He, Zhaopeng Tu, Xing Wang, Longyue Wang, Michael Lyu and Shuming Shi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3857" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4056"><td><span class="poster-title">Multilingual Neural Machine Translation with Language Clustering. </span><em>Xu Tan, Jiale Chen, Di He, Yingce Xia, Tao QIN and Tie-Yan Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4056" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1065"><td><span class="poster-title">Don't Forget the Long Tail! A Comprehensive Analysis of Morphological Generalization in Bilingual Lexicon Induction. </span><em>Paula Czarnowska, Sebastian Ruder, Edouard Grave, Ryan Cotterell and Ann Copestake</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1065" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1268"><td><span class="poster-title">A Functionalist Account of Vowel System Typology. </span><em>Ryan Cotterell and Jason Eisner</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1268" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2230"><td><span class="poster-title">Pushing the Limits of Low-Resource Morphological Inflection. </span><em>Antonios Anastasopoulos and Graham Neubig</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2230" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="TACL-1654"><td><span class="poster-title">Morphological Analysis Using a Sequence Decoder. </span><em>Ekin Akyürek, Erenay Dayanık and Deniz Yuret</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1654" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="205"><td><span class="poster-title">Cross-Lingual Dependency Parsing Using Code-Mixed TreeBank. </span><em>Meishan Zhang, Yue Zhang and Guohong Fu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-205" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="531"><td><span class="poster-title">Hierarchical Pointer Net Parsing. </span><em>Linlin Liu, Xiang Lin, Shafiq Joty, Simeng Han and Lidong Bing</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-531" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="719"><td><span class="poster-title">Semi-Supervised Semantic Role Labeling with Cross-View Training. </span><em>Rui Cai and Mirella Lapata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-719" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="809"><td><span class="poster-title">Low-Resource Sequence Labeling via Unsupervised Multilingual Contextualized Representations. </span><em>Zuyi Bao, Rui Huang, Chen Li and Kenny Zhu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-809" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="863"><td><span class="poster-title">A Lexicon-Based Graph Neural Network for Chinese NER. </span><em>Tao Gui, Yicheng Zou, Qi Zhang, Minlong Peng, Jinlan Fu, Zhongyu Wei and Xuanjing Huang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-863" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1556"><td><span class="poster-title">CM-Net: A Novel Collaborative Memory Network for Spoken Language Understanding. </span><em>Yijin Liu, Fandong Meng, Jinchao Zhang, Jie Zhou, Yufeng Chen and Jinan Xu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1556" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1794"><td><span class="poster-title">Tree Transformer: Integrating Tree Structures into Self-Attention. </span><em>Yaushian Wang, Hung-Yi Lee and Yun-Nung Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1794" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2179"><td><span class="poster-title">Semantic Role Labeling with Iterative Structure Refinement. </span><em>Chunchuan Lyu, Shay B. Cohen and Ivan Titov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2179" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2724"><td><span class="poster-title">Entity Projection via Machine Translation for Cross-Lingual NER. </span><em>Alankar Jain, Bhargavi Paranjape and Zachary C. Lipton</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2724" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2738"><td><span class="poster-title">A Bayesian Approach for Sequence Tagging with Crowds. </span><em>Edwin D. Simpson and Iryna Gurevych</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2738" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3091"><td><span class="poster-title">A systematic comparison of methods for low-resource dependency parsing on genuinely low-resource languages. </span><em>Clara Vania, Yova Kementchedjhieva, Anders Søgaard and Adam Lopez</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3091" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3368"><td><span class="poster-title">Target Language-Aware Constrained Inference for Cross-lingual Dependency Parsing. </span><em>Tao Meng, Nanyun Peng and Kai-Wei Chang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3368" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3711"><td><span class="poster-title">Look-up and Adapt: A One-shot Semantic Parser. </span><em>Zhichu Lu, Forough Arabshahi, Igor Labutov and Tom Mitchell</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3711" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3886"><td><span class="poster-title">Similarity Based Auxiliary Classifier for Named Entity Recognition. </span><em>Shiyuan Xiao, Yuanxin Ouyang, Wenge Rong, Jianxin Yang and Zhang Xiong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3886" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4015"><td><span class="poster-title">Variable beam search for generative neural parsing and its relevance for the analysis of neuro-imaging signal. </span><em>Benoit Crabbé, Murielle Fabre and Christophe Pallier</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4015" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-29"><td><span class="poster-title">MY-AKKHARA: A Romanization-based Burmese (Myanmar) Input Method. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-29" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-33"><td><span class="poster-title">LINSPECTOR WEB: A Multilingual Probing Suite for Word Representations. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-33" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-40"><td><span class="poster-title">Joey NMT: A Minimalist NMT Toolkit for Novices. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-40" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-59"><td><span class="poster-title">Multilingual, Multi-scale and Multi-layer Visualization of Intermediate Representations. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-59" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-65"><td><span class="poster-title">A System for Diacritizing Four Varieties of Arabic. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-65" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-75"><td><span class="poster-title">What's Wrong with Hebrew NLP? And How to Make it Right. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-75" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-100"><td><span class="poster-title">INMT: Interactive Neural Machine Translation Prediction. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-100" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-break-2"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Tuesday, 5 November 2019">15:00 &ndash; 15:30</span></div>
<div class="session-box" id="session-box-3"><div class="session-header" id="session-header-3"> (Session 3)</div>
<div class="session session-expandable session-papers1" id="session-3a"><div id="expander"></div><a href="#" class="session-title">3A: Machine Learning II</a><br/><span class="session-time" title="Tuesday, 5 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1092"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Are We Modeling the Task or the Annotator? An Investigation of Annotator Bias in Natural Language Understanding Datasets. </span><em>Mor Geva, Yoav Goldberg and Jonathan Berant</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1092" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1128"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Robust Text Classifier on Test-Time Budgets. </span><em>Md Rizwan Parvez, Tolga Bolukbasi, Kai-Wei Chang and Venkatesh Saligrama</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1128" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3289"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Commonsense Knowledge Mining from Pretrained Models. </span><em>Joe Davison, Joshua Feldman and Alexander Rush</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3289" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3428"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">RNN Architecture Learning with Sparse Regularization. </span><em>Jesse Dodge, Roy Schwartz, Hao Peng and Noah A. Smith</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3428" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-3b"><div id="expander"></div><a href="#" class="session-title">3B: Semantics</a><br/><span class="session-time" title="Tuesday, 5 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="75"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Analytical Methods for Interpretable Ultradense Word Embeddings. </span><em>Philipp Dufter and Hinrich Schütze</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-75" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3142"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Investigating Meta-Learning Algorithms for Low-Resource Natural Language Understanding Tasks. </span><em>Zi-Yi Dou, Keyi Yu and Antonios Anastasopoulos</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3142" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3045"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Retrofitting Contextualized Word Embeddings with Paraphrases. </span><em>Weijia Shi, Muhao Chen, Pei Zhou and Kai-Wei Chang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3045" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3508"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">Incorporating Contextual and Syntactic Structures Improves Semantic Similarity Modeling. </span><em>Linqing Liu, Wei Yang, Jinfeng Rao, Raphael Tang and Jimmy Lin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3508" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-3c"><div id="expander"></div><a href="#" class="session-title">3C: Discourse, Summarization, &amp; Generation</a><br/><span class="session-time" title="Tuesday, 5 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3399"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Neural Linguistic Steganography. </span><em>Zachary Ziegler, Yuntian Deng and Alexander Rush</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3399" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3018"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">The Feasibility of Embedding Based Automatic Evaluation for Single Document Summarization. </span><em>Simeng Sun and Ani Nenkova</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3018" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1918"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Attention Optimization for Abstractive Document Summarization. </span><em>Min Gui, Junfeng Tian, Rui Wang and Zhenglu Yang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1918" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2020"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">Rewarding Coreference Resolvers for Being Consistent with World Knowledge. </span><em>Rahul Aralikatte, Heather Lent, Ana Valeria Gonzalez, Daniel Herschcovich, Chen Qiu, Anders Sandholm, Michael Ringaard and Anders Søgaard</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2020" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-3d"><div id="expander"></div><a href="#" class="session-title">3D: Text Mining &amp; NLP Applications I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-3d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-3d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="740"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">An Empirical Study of Incorporating Pseudo Data into Grammatical Error Correction. </span><em>Shun Kiyono, Jun Suzuki, Masato Mita, Tomoya Mizumoto and Kentaro Inui</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-740" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1257"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">A Multilingual Topic Model for Learning Weighted Topic Links Across Corpora with Low Comparability. </span><em>Weiwei Yang, Jordan Boyd-Graber and Philip Resnik</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1257" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3730"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Measure Country-Level Socio-Economic Indicators with Streaming News: An Empirical Study. </span><em>Bonan Min and Xiaoxi Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3730" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2903"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">Towards Extracting Medical Family History from Natural Language Interactions: A New Dataset and Baselines. </span><em>Mahmoud Azab, Stephane Dadian, Vivi Nastase, Larry An and Rada Mihalcea</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2903" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-3"><div id="expander"></div><a href="#" class="session-title">3 Poster & Demo: Dialog &amp; Interactive Systems, Machine Translation &amp; Multilinuality, Phonology, Morphology, &amp; Word Segmentation, Speech, Vision, Robotics, Multimodal &amp; Grounding, Tagging, Chunking, Syntax &amp; Parsing </a><br/><span class="session-time" title="Tuesday, 5 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="242"><td><span class="poster-title">Multi-task Learning for Natural Language Generation in Task-Oriented Dialogue. </span><em>Chenguang Zhu, Michael Zeng and Xuedong Huang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-242" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="622"><td><span class="poster-title">Dirichlet Latent Variable Hierarchical Recurrent Encoder-Decoder in Dialogue Generation. </span><em>Min Zeng, Yisen Wang and Yuan Luo</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-622" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1011"><td><span class="poster-title">Semi-Supervised Bootstrapping of Dialogue State Trackers for Task-Oriented Modelling. </span><em>Bo-Hsiang Tseng, Marek Rei, Paweł Budzianowski, Richard Turner, Bill Byrne and Anna Korhonen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1011" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1289"><td><span class="poster-title">A Progressive Model to Enable Continual Learning for Semantic Slot Filling. </span><em>Yilin Shen, Xiangyu Zeng and Hongxia Jin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1289" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1447"><td><span class="poster-title">CASA-NLU: Context-Aware Self-Attentive Natural Language Understanding for Task-Oriented Chatbots. </span><em>Arshit Gupta, Peng Zhang, Garima Lalwani and Mona Diab</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1447" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2050"><td><span class="poster-title">Sampling Matters! An Empirical Study of Negative Sampling Strategies for Learning of Matching Models in Retrieval-based Dialogue Systems. </span><em>Jia Li, Chongyang Tao, wei wu, Yansong Feng, Dongyan Zhao and Rui Yan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2050" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2329"><td><span class="poster-title">Zero-shot Cross-lingual Dialogue Systems with Transferable Latent Variables. </span><em>Zihan Liu, Jamin Shin, Yan Xu, Genta Indra Winata, Peng Xu, Andrea Madotto and Pascale Fung</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2329" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2650"><td><span class="poster-title">Modeling Multi-Action Policy for Task-Oriented Dialogues. </span><em>Lei Shu, Hu Xu, Bing Liu and Piero Molino</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2650" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3471"><td><span class="poster-title">An Evaluation Dataset for Intent Classification and Out-of-Scope Prediction. </span><em>Stefan Larson, Anish Mahendran, Joseph J. Peper, Christopher Clarke, Andrew Lee, Parker Hill, Jonathan K. Kummerfeld, Kevin Leach, Michael A. Laurenzano, Lingjia Tang and Jason mars</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3471" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3528"><td><span class="poster-title">Automatically Learning Data Augmentation Policies for Dialogue Tasks. </span><em>Tong Niu and Mohit Bansal</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3528" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="351"><td><span class="poster-title">uniblock: Scoring and Filtering Corpus with Unicode Block Information. </span><em>Yingbo Gao, Weiyue Wang and Hermann Ney</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-351" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="533"><td><span class="poster-title">Multilingual word translation using auxiliary languages. </span><em>Hagai Taitelbaum, Gal Chechik and Jacob Goldberger</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-533" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="801"><td><span class="poster-title">Towards Better Modeling Hierarchical Structure for Self-Attention with Ordered Neurons. </span><em>Jie Hao, Xing Wang, Shuming Shi, Jinfeng Zhang and Zhaopeng Tu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-801" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1284"><td><span class="poster-title">Vecalign: Improved Sentence Alignment in Linear Time and Space. </span><em>Brian Thompson and Philipp Koehn</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1284" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1603"><td><span class="poster-title">Simpler and Faster Learning of Adaptive Policies for Simultaneous Translation. </span><em>Baigong Zheng, Renjie Zheng, Mingbo Ma and Liang Huang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1603" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1889"><td><span class="poster-title">Adversarial Learning with Contextual Embeddings for Zero-resource Cross-lingual Classification and NER. </span><em>Phillip Keung, yichao lu and Vikas Bhardwaj</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1889" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2114"><td><span class="poster-title">Recurrent Positional Embedding for Neural Machine Translation. </span><em>Kehai Chen, Rui Wang, Masao Utiyama and Eiichiro Sumita</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2114" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2413"><td><span class="poster-title">Machine Translation for Machines: the Sentiment Classification Use Case. </span><em>amirhossein tebbifakhr, Luisa Bentivogli, Matteo Negri and Marco Turchi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2413" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2552"><td><span class="poster-title">Investigating the Effectiveness of BPE: The Power of Shorter Sequences. </span><em>Matthias Gallé</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2552" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3022"><td><span class="poster-title">HABLex: Human Annotated Bilingual Lexicons for Experiments in Machine Translation. </span><em>Brian Thompson, Rebecca Knowles, Xuan Zhang, Huda Khayrallah, Kevin Duh and Philipp Koehn</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3022" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3336"><td><span class="poster-title">Handling Syntactic Divergence in Low-resource Machine Translation. </span><em>Chunting Zhou, Xuezhe Ma, Junjie Hu and Graham Neubig</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3336" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3487"><td><span class="poster-title">Speculative Beam Search for Simultaneous Translation. </span><em>Renjie Zheng, Mingbo Ma, Baigong Zheng and Liang Huang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3487" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3548"><td><span class="poster-title">Self-Attention with Structural Position Representations. </span><em>Xing Wang, Zhaopeng Tu, Longyue Wang and Shuming Shi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3548" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3590"><td><span class="poster-title">Exploiting Multilingualism through Multistage Fine-Tuning for Low-Resource Neural Machine Translation. </span><em>Raj Dabre, Atsushi Fujita and Chenhui Chu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3590" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3716"><td><span class="poster-title">Unsupervised Domain Adaptation for Neural Machine Translation with Domain-Aware Feature Embeddings. </span><em>Zi-Yi Dou, Junjie Hu, Antonios Anastasopoulos and Graham Neubig</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3716" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4061"><td><span class="poster-title">A Regularization-based Framework for Bilingual Grammar Induction. </span><em>Yong Jiang, Wenjuan Han and Kewei Tu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4061" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4083"><td><span class="poster-title">Encoders Help You Disambiguate Word Senses in Neural Machine Translation. </span><em>Gongbo Tang, Rico Sennrich and Joakim Nivre</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4083" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2376"><td><span class="poster-title">Korean Morphological Analysis with Tied Sequence-to-Sequence Multi-Task Model. </span><em>Hyun-Je Song and Seong-Bae Park</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2376" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3733"><td><span class="poster-title">Efficient Convolutional Neural Networks for Diacritic Restoration. </span><em>Sawsan Alqahtani, Ajay Mishra and Mona Diab</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3733" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="459"><td><span class="poster-title">Improving Generative Visual Dialog by Answering Diverse Questions. </span><em>Vishvak Murahari, Prithvijit Chattopadhyay, Dhruv Batra, Devi Parikh and Abhishek Das</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-459" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="790"><td><span class="poster-title">Cross-lingual Transfer Learning with Data Selection for Large-Scale Spoken Language Understanding. </span><em>Quynh Do and Judith Gaspers</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-790" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2786"><td><span class="poster-title">Multi-Head Attention with Diversity for Learning Grounded Multilingual Multimodal Representations. </span><em>Po-Yao Huang, Xiaojun Chang and Alexander Hauptmann</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2786" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3263"><td><span class="poster-title">Decoupled Box Proposal and Featurization with Ultrafine-Grained Semantic Labels Improve Image Captioning and Visual Question Answering. </span><em>Soravit Changpinyo, Bo Pang, Piyush Sharma and Radu Soricut</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3263" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3293"><td><span class="poster-title">REO-Relevance, Extraness, Omission: A Fine-grained Evaluation for Image Captioning. </span><em>Ming Jiang, Junjie Hu, Qiuyuan Huang, Lei Zhang, Jana Diesner and Jianfeng Gao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3293" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3398"><td><span class="poster-title">WSLLN:Weakly Supervised Natural Language Localization Networks. </span><em>Mingfei Gao, Larry Davis, Richard Socher and Caiming Xiong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3398" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3748"><td><span class="poster-title">Grounding learning of modifier dynamics: An application to color naming. </span><em>Xudong Han, Philip Schulz and Trevor Cohn</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3748" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3830"><td><span class="poster-title">Robust Navigation with Language Pretraining and Stochastic Sampling. </span><em>Xiujun Li, Chunyuan Li, Qiaolin Xia, Yonatan Bisk, Asli Celikyilmaz, Jianfeng Gao, Noah A. Smith and Yejin Choi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3830" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="413"><td><span class="poster-title">Towards Making a Dependency Parser See. </span><em>Michalina Strzyz, David Vilares and Carlos Gómez-Rodríguez</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-413" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1234"><td><span class="poster-title">Unsupervised Labeled Parsing with Deep Inside-Outside Recursive Autoencoders. </span><em>Andrew Drozdov, Patrick Verga, Yi-Pei Chen, Mohit Iyyer and Andrew McCallum</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1234" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3171"><td><span class="poster-title">Dependency Parsing for Spoken Dialog Systems. </span><em>Sam Davidson, Dian Yu and Zhou Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3171" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3240"><td><span class="poster-title">Span-based Hierarchical Semantic Parsing for Task-Oriented Dialog. </span><em>Panupong Pasupat, Sonal Gupta, Karishma Mandyam, Rushin Shah, Mike Lewis and Luke Zettlemoyer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3240" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-break-3"><span class="session-title">Mini-Break</span><br/><span class="session-time" title="Tuesday, 5 November 2019">16:18 &ndash; 16:30</span></div>
<div class="session-box" id="session-box-4"><div class="session-header" id="session-header-4"> (Session 4)</div>
<div class="session session-expandable session-papers1" id="session-4a"><div id="expander"></div><a href="#" class="session-title">4A: Neural Machine Translation</a><br/><span class="session-time" title="Tuesday, 5 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2416"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Enhancing Context Modeling with a Query-Guided Capsule Network for Document-level Translation. </span><em>Zhengxin Yang, Jinchao Zhang, Fandong Meng, Shuhao Gu, Yang Feng and Jie Zhou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2416" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3252"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Simple, Scalable Adaptation for Neural Machine Translation. </span><em>Ankur Bapna and Orhan Firat</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3252" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3177"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Controlling Text Complexity in Neural Machine Translation. </span><em>Sweta Agrawal and Marine Carpuat</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3177" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1388"><td id="paper-time">17:24&ndash;17:42</td><td><span class="paper-title">Investigating Multilingual NMT Representations at Scale. </span><em>Sneha Kudugunta, Ankur Bapna, Isaac Caswell and Orhan Firat</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1388" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1423"><td id="paper-time">17:42&ndash;18:00</td><td><span class="paper-title">Hierarchical Modeling of Global Context for Document-Level Neural Machine Translation. </span><em>Xin Tan, Longyin Zhang, Deyi Xiong and Guodong Zhou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1423" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-4b"><div id="expander"></div><a href="#" class="session-title">4B: Question Answering I</a><br/><span class="session-time" title="Tuesday, 5 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="8"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Cross-Lingual Machine Reading Comprehension. </span><em>Yiming Cui, Wanxiang Che, Ting Liu, Bing Qin, Shijin Wang and Guoping Hu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-8" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="582"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">A Multi-Type Multi-Span Network for Reading Comprehension that Requires Discrete Reasoning. </span><em>Minghao Hu, Yuxing Peng, Zhen Huang and Dongsheng Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-582" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="880"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Neural Duplicate Question Detection without Labeled Training Data. </span><em>Andreas Rücklé, Nafise Sadat Moosavi and Iryna Gurevych</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-880" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="889"><td id="paper-time">17:24&ndash;17:42</td><td><span class="paper-title">Asking Clarification Questions in Knowledge-Based Question Answering. </span><em>Jingjing Xu, Yuechen Wang, Duyu Tang, Nan Duan, Pengcheng Yang, Qi Zeng, Ming Zhou and Xu SUN</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-889" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1646"><td id="paper-time">17:42&ndash;18:00</td><td><span class="paper-title">Multi-View Domain Adapted Sentence Embeddings for Low-Resource Unsupervised Duplicate Question Detection. </span><em>Nina Poerner and Hinrich Schütze</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1646" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-4c"><div id="expander"></div><a href="#" class="session-title">4C: Social Media &amp; Computational Social Science</a><br/><span class="session-time" title="Tuesday, 5 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="172"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Multi-label Categorization of Accounts of Sexism using a Neural Framework. </span><em>Pulkit Parikh, Harika Abburi, Pinkesh Badjatiya, Radhika Krishnan, Niyati Chhaya, Manish Gupta and Vasudeva Varma</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-172" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1462"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">The Trumpiest Trump? Identifying a Subject's Most Characteristic Tweets. </span><em>Charuta Pethe and Steve Skiena</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1462" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2950"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Finding Microaggressions in the Wild: A Case for Locating Elusive Phenomena in Social Media Posts. </span><em>Luke Breitfeller, Emily Ahn, David Jurgens and Yulia Tsvetkov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2950" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="694"><td id="paper-time">17:24&ndash;17:42</td><td><span class="paper-title">Reinforced Product Metadata Selection for Helpfulness Assessment of Customer Reviews. </span><em>Miao Fan, Chao Feng, Mingming Sun and Ping Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-694" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3557"><td id="paper-time">17:42&ndash;18:00</td><td><span class="paper-title">Learning Invariant Representations of Social Media Users. </span><em>Nicholas Andrews and Marcus Bishop</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3557" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-4d"><div id="expander"></div><a href="#" class="session-title">4D: Text Mining &amp; NLP Applications II</a><br/><span class="session-time" title="Tuesday, 5 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-4d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-4d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3793"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">(Male, Bachelor) and (Female, Ph.D) have different connotations: Parallelly Annotated Stylistic Language Dataset with Multiple Personas. </span><em>Dongyeop Kang, Varun Gangal and Eduard Hovy</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3793" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="244"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Movie Plot Analysis via Turning Point Identification. </span><em>Pinelopi Papalampidi, Frank Keller and Mirella Lapata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-244" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2488"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Latent Suicide Risk Detection on Microblog via Suicide-Oriented Word Embeddings and Layered Attention. </span><em>Lei Cao, Huijun Zhang, Ling Feng, Zihan Wei, Xin Wang, Ningyun Li and Xiaohao He</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2488" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1903"><td id="paper-time">17:24&ndash;17:42</td><td><span class="paper-title">Deep Ordinal Regression for Pledge Specificity Prediction. </span><em>Shivashankar Subramanian, Trevor Cohn and Timothy Baldwin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1903" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="TACL-1677"><td id="paper-time">17:42&ndash;18:00</td><td><span class="paper-title">Enabling Robust Grammatical Error Correction in New Domains: Datasets, Metrics, and Analyses. </span><em>Courtney Napoles, Maria Nadejde and Joel Tetreault</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1677" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-4"><div id="expander"></div><a href="#" class="session-title">4 Poster & Demo: Dialog &amp; Interactive Systems, Speech, Vision, Robotics, Multimodal &amp; Grounding </a><br/><span class="session-time" title="Tuesday, 5 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="9"><td><span class="poster-title">Data-Efficient Goal-Oriented Conversation with Dialogue Knowledge Transfer Networks. </span><em>Igor Shalyminov, Sungjin Lee, Arash Eshghi and Oliver Lemon</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-9" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="64"><td><span class="poster-title">Multi-Granularity Representations of Dialog. </span><em>Shikib Mehri and Maxine Eskenazi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-64" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="111"><td><span class="poster-title">Are You for Real? Detecting Identity Fraud via Dialogue Interactions. </span><em>Weikang Wang, Jiajun Zhang, Qian Li, Chengqing Zong and Zhifei Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-111" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="124"><td><span class="poster-title">Hierarchy Response Learning for Neural Conversation Generation. </span><em>Bo Zhang and Xiaoming Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-124" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="138"><td><span class="poster-title">Knowledge Aware Conversation Generation with Explainable Reasoning over Augmented Graphs. </span><em>zhibin liu, Zheng-Yu Niu, Hua Wu and Haifeng Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-138" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="298"><td><span class="poster-title">Adaptive Parameterization for Neural Dialogue Generation. </span><em>Hengyi Cai, Hongshen Chen, Cheng Zhang, Yonghao Song, Xiaofang Zhao and Dawei Yin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-298" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="316"><td><span class="poster-title">Towards Knowledge-Based Recommender Dialog System. </span><em>Qibin Chen, Junyang Lin, Yichang Zhang, Ming Ding, Yukuo Cen, Hongxia Yang and Jie Tang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-316" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="419"><td><span class="poster-title">Structuring Latent Spaces for Stylized Response Generation. </span><em>Xiang Gao, Yizhe Zhang, Sungjin Lee, Michel Galley, Chris Brockett, Jianfeng Gao and Bill Dolan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-419" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="537"><td><span class="poster-title">Improving Open-Domain Dialogue Systems via Multi-Turn Incomplete Utterance Restoration. </span><em>Zhufeng Pan, Kun Bai, Yan Wang, Lianqiang Zhou and Xiaojiang Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-537" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="771"><td><span class="poster-title">Unsupervised Context Rewriting for Open Domain Conversation. </span><em>Kun Zhou, Kai Zhang, Yu Wu, Shujie Liu and Jingsong Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-771" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="866"><td><span class="poster-title">Dually Interactive Matching Network for Personalized Response Selection in Retrieval-Based Chatbots. </span><em>Jia-Chen Gu, Zhen-Hua Ling, Xiaodan Zhu and Quan Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-866" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1432"><td><span class="poster-title">DyKgChat: Benchmarking Dialogue Generation Grounding on Dynamic Knowledge Graphs. </span><em>Yi-Lin Tuan, Yun-Nung Chen and Hung-yi Lee</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1432" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1550"><td><span class="poster-title">Retrieval-guided Dialogue Response Generation via a Matching-to-Generation Framework. </span><em>Deng Cai, Yan Wang, Wei Bi, Zhaopeng Tu, Xiaojiang Liu and Shuming Shi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1550" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1842"><td><span class="poster-title">Scalable and Accurate Dialogue State Tracking via Hierarchical Sequence Generation. </span><em>Liliang Ren, Jianmo Ni and Julian McAuley</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1842" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1931"><td><span class="poster-title">Low-Resource Response Generation with Template Prior. </span><em>Ze Yang, wei wu, Jian Yang, Can Xu and zhoujun li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1931" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2039"><td><span class="poster-title">A Discrete CVAE for Response Generation on Short-Text Conversation. </span><em>Jun Gao, Wei Bi, Xiaojiang Liu, Junhui Li, Guodong Zhou and Shuming Shi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2039" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2495"><td><span class="poster-title">Who Is Speaking to Whom? Learning to Identify Utterance Addressee in Multi-Party Conversations. </span><em>Ran Le, Wenpeng Hu, Mingyue Shang, Zhenjun You, Lidong Bing, Dongyan Zhao and Rui Yan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2495" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2594"><td><span class="poster-title">A Semi-Supervised Stable Variational Network for Promoting Replier-Consistency in Dialogue Generation. </span><em>Jinxin Chang, Ruifang He, Longbiao Wang, Xiangyu Zhao, Ting Yang and Ruifang Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2594" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2685"><td><span class="poster-title">Modeling Personalization in Continuous Space for Response Generation via Augmented Wasserstein Autoencoders. </span><em>Zhangming Chan, Juntao Li, Xiaopeng Yang, Xiuying Chen, Wenpeng Hu, Dongyan Zhao and Rui Yan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2685" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3513"><td><span class="poster-title">Variational Hierarchical User-based Conversation Model. </span><em>JinYeong Bak and Alice Oh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3513" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3727"><td><span class="poster-title">Recommendation as a Communication Game: Self-Supervised Bot-Play for Goal-oriented Dialogue. </span><em>Dongyeop Kang, Anusha Balakrishnan, Pararth Shah, Paul Crook, Y-Lan Boureau and Jason Weston</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3727" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3881"><td><span class="poster-title">CoSQL: A Conversational Text-to-SQL Challenge Towards Cross-Domain Natural Language Interfaces to Databases. </span><em>Tao Yu, Rui Zhang, Heyang Er, Suyi Li, Eric Xue, Bo Pang, Xi Victoria Lin, Yi Chern Tan, Tianze Shi, Zihan Li, Youxuan Jiang, Michihiro Yasunaga, Sungrok Shim, Tao Chen, Alexander Fabbri, Zifan Li, Luyao Chen, Yuwen Zhang, Shreya Dixit, Vincent Zhang, Caiming Xiong, Richard Socher, Walter Lasecki and Dragomir Radev</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3881" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3954"><td><span class="poster-title">A Practical Dialogue-Act-Driven Conversation Model for Multi-Turn Response Selection. </span><em>Harshit Kumar, Arvind Agarwal and Sachindra Joshi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3954" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4003"><td><span class="poster-title">How to Build User Simulators to Train RL-based Dialog Systems. </span><em>Weiyan Shi, Kun Qian, Xuewei Wang and Zhou Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4003" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="TACL-1676"><td><span class="poster-title">Graph Convolutional Network with Sequential Attention for Goal-Oriented Dialogue Systems. </span><em>Suman Banerjee and Mitesh M. Khapra</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1676" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="294"><td><span class="poster-title">Low-Rank HOCA: Efficient High-Order Cross-Modal Attention for Video Captioning. </span><em>Tao Jin, Siyu Huang, Yingming Li and Zhongfei Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-294" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="370"><td><span class="poster-title">Image Captioning with Very Scarce Supervised Data: Adversarial Semi-Supervised Learning Approach. </span><em>Dong-Jin Kim, Jinsoo Choi, Tae-Hyun Oh and In So Kweon</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-370" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="401"><td><span class="poster-title">Dual Attention Networks for Visual Reference Resolution in Visual Dialog. </span><em>Gi-Cheon Kang, Jaeseo Lim and Byoung-Tak Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-401" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="942"><td><span class="poster-title">Unsupervised Discovery of Multimodal Links in Multi-image, Multi-sentence Documents. </span><em>Jack Hessel, Lillian Lee and David Mimno</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-942" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="996"><td><span class="poster-title">UR-FUNNY: A Multimodal Language Dataset for Understanding Humor. </span><em>Md Kamrul Hasan, Wasifur Rahman, AmirAli Bagher Zadeh, Jianyuan Zhong, Md Iftekhar Tanveer, Louis-Philippe Morency and Mohammed (Ehsan) Hoque</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-996" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1923"><td><span class="poster-title">Partners in Crime: Multi-view Sequential Inference for Movie Understanding. </span><em>Nikos Papasarantopoulos, Lea Frermann, Mirella Lapata and Shay B. Cohen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1923" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2097"><td><span class="poster-title">Guiding the Flowing of Semantics: Interpretable Video Captioning via POS Tag. </span><em>Xinyu Xiao, Lingfeng Wang, Bin Fan, Shinming Xiang and Chunhong Pan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2097" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2414"><td><span class="poster-title">A Stack-Propagation Framework with Token-Level Intent Detection for Spoken Language Understanding. </span><em>Libo Qin, Wanxiang Che, Yangming Li, Haoyang Wen and Ting Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2414" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2718"><td><span class="poster-title">Talk2Car: Taking Control of Your Self-Driving Car. </span><em>Thierry Deruyttere, Simon Vandenhende, Dusan Grujicic, Luc Van Gool and Marie-Francine Moens</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2718" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2739"><td><span class="poster-title">Fact-Checking Meets Fauxtography: Verifying Claims About Images. </span><em>Dimitrina Zlatkova, Preslav Nakov and Ivan Koychev</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2739" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2766"><td><span class="poster-title">Video Dialog via Progressive Inference and Cross-Transformer. </span><em>Weike Jin, Zhou Zhao, Mao Gu, Jun Xiao, Furu Wei and Yueting Zhuang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2766" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2884"><td><span class="poster-title">Executing Instructions in Situated Collaborative Interactions. </span><em>Alane Suhr, Claudia Yan, Jack Schluger, Stanley Yu, Hadi Khader, Marwa Mouallem, Iris Zhang and Yoav Artzi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2884" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3099"><td><span class="poster-title">Fusion of Detected Objects in Text for Visual Question Answering. </span><em>Chris Alberti, Jeffrey Ling, Michael Collins and David Reitter</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3099" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3260"><td><span class="poster-title">TIGEr: Text-to-Image Grounding for Image Caption Evaluation. </span><em>Ming Jiang, Qiuyuan Huang, Lei Zhang, Xin Wang, Pengchuan Zhang, Zhe Gan, Jana Diesner and Jianfeng Gao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3260" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-38"><td><span class="poster-title">EGG: a toolkit for research on Emergence of lanGuage in Games. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-38" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-43"><td><span class="poster-title">Chameleon: A Language Model Adaptation Toolkit for Automatic Speech Recognition of Conversational Speech. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-43" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-60"><td><span class="poster-title">PyOpenDial: A Python-based Domain-Independent Toolkit for Developing Spoken Dialogue Systems with Probabilistic Rules. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-60" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-67"><td><span class="poster-title">PolyResponse: A Rank-based Approach to Task-Oriented Dialogue with Application in Restaurant Search and Booking. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-67" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-71"><td><span class="poster-title">LIDA: Lightweight Interactive Dialogue Annotator. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-71" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-88"><td><span class="poster-title">Entity resolution for noisy ASR transcripts. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-88" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-103"><td><span class="poster-title">Gunrock: A Social Bot for Complex and Engaging Long Conversations. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-103" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-115"><td><span class="poster-title">HARE: a Flexible Highlighting Annotator for Ranking and Exploration. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-115" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="day" id="day-4">Wednesday, 6 November 2019</div>
<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>Keynote II: "Current Challenges in Computational Social Science"</strong></a><br/><span class="session-people"><a href="https://ds.kaist.ac.kr/professor.html" target="_blank">Meeyoung Cha (KAIST)</a></span><br/><span class="session-time" title="Wednesday, 6 November 2019">09:00 &ndash; 10:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><div class="paper-session-details"><br/><div class="session-abstract"><p>Artificial intelligence (AI) is reshaping business and science. Computational social science is an interdisciplinary field that solves complex societal problems by adopting AI-driven methods, processes, algorithms, and systems on data of various forms. This talk will review some of the latest advances in the research that focuses on fake news and legal liability. I will first discuss the structural, temporal, and linguistic traits of fake news propagation. One emerging challenge here is the increasing use of automated bots to generate and propagate false information. I will also discuss the current issues on the legal liability of AI and robots, particularly on how to regulate them (e.g., moral machine, punishment gap). This talk will suggest new opportunities to tackle these problems.</p></div></div></div>
<div class="session session-break session-plenary" id="session-break-4"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Wednesday, 6 November 2019">10:00 &ndash; 10:30</span></div>
<div class="session-box" id="session-box-5"><div class="session-header" id="session-header-5"> (Session 5)</div>
<div class="session session-expandable session-papers1" id="session-5a"><div id="expander"></div><a href="#" class="session-title">5A: Machine Learning III</a><br/><span class="session-time" title="Wednesday, 6 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1515"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Universal Adversarial Triggers for Attacking and Analyzing NLP. </span><em>Eric Wallace, Shi Feng, Nikhil Kandpal, Matt Gardner and Sameer Singh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1515" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2756"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">To Annotate or Not? Predicting Performance Drop under Domain Shift. </span><em>Hady Elsahar and Matthias Gallé</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2756" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2900"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Adaptively Sparse Transformers. </span><em>Gonçalo M. Correia, Vlad Niculae and André F. T. Martins</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2900" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3277"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Show Your Work:  Improved Reporting of Experimental Results. </span><em>Jesse Dodge, Suchin Gururangan, Dallas Card, Roy Schwartz and Noah A. Smith</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3277" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3999"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">A Deep Factorization of Style and Structure in Fonts. </span><em>Akshay Srivatsan, Jonathan Barron, Dan Klein and Taylor Berg-Kirkpatrick</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3999" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-5b"><div id="expander"></div><a href="#" class="session-title">5B: Lexical Semantics II</a><br/><span class="session-time" title="Wednesday, 6 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1735"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Cross-lingual Semantic Specialization via Lexical Relation Induction. </span><em>Edoardo Maria Ponti, Ivan Vulić, Goran Glavaš, Roi Reichart and Anna Korhonen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1735" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2670"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Modelling the interplay of metaphor and emotion through multitask learning. </span><em>Verna Dankers, Marek Rei, Martha Lewis and Ekaterina Shutova</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2670" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3460"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">How well do NLI models capture verb veridicality?. </span><em>Alexis Ross and Ellie Pavlick</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3460" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3515"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Modeling Color Terminology Across Thousands of Languages. </span><em>Arya D. McCarthy, Winston Wu, Aaron Mueller, William Watson and David Yarowsky</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3515" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1314"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Negative Focus Detection via Contextual Attention Mechanism. </span><em>Longxiang Shen, Bowei Zou, Yu Hong, Guodong Zhou, Qiaoming Zhu and AiTi Aw</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1314" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-5c"><div id="expander"></div><a href="#" class="session-title">5C: Discourse &amp; Pragmatics</a><br/><span class="session-time" title="Wednesday, 6 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1792"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">A Unified Neural Coherence Model. </span><em>Han Cheol Moon, Tasnim Mohiuddin, Shafiq Joty and Chi Xu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1792" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2642"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Topic-Guided Coherence Modeling for Sentence Ordering by Preserving Global and Local Information. </span><em>Byungkook Oh, Seungmin Seo, Cheolheon Shin, Eunju Jo and Kyong-Ho Lee</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2642" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="4060"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Neural Generative Rhetorical Structure Parsing. </span><em>Amandla Mabona, Laura Rimell, Stephen Clark and Andreas Vlachos</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4060" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2453"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Weak Supervision for Learning Discourse Structure. </span><em>Sonia Badene, Kate Thompson, Jean-Pierre Lorré and Nicholas Asher</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2453" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2625"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Predicting Discourse Structure using Distant Supervision from Sentiment. </span><em>Patrick Huber and Giuseppe Carenini</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2625" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-5d"><div id="expander"></div><a href="#" class="session-title">5D: Text Mining &amp; NLP Applications III</a><br/><span class="session-time" title="Wednesday, 6 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-5d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-5d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2233"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">The Myth of Double-Blind Review Revisited: ACL vs. EMNLP. </span><em>Cornelia Caragea, Ana Uban and Liviu P. Dinu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2233" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2653"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Uncover Sexual Harassment Patterns from Personal Stories by Joint Key Element Extraction and Categorization. </span><em>Yingchi Liu, Quanzhi Li, Marika Cifor, Xiaozhong Liu, Qiong Zhang and Luo Si</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2653" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2864"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Identifying Predictive Causal Factors from News Streams. </span><em>Ananth Balashankar, Sunandan Chakraborty, Samuel Fraiberger and Lakshminarayanan Subramanian</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2864" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3011"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Training Data Augmentation for Detecting Adverse Drug Reactions in User-Generated Content. </span><em>Sepideh Mesbah, Jie Yang, Robert-Jan Sips, Manuel Valle Torre, Christoph Lofi, Alessandro Bozzon and Geert-Jan Houben</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3011" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3160"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Deep Reinforcement Learning-based Text Anonymization against Private-Attribute Inference. </span><em>Ahmadreza Mosallanezhad, Ghazaleh Beigi and Huan Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3160" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-5"><div id="expander"></div><a href="#" class="session-title">5 Poster & Demo: Question Answering, Textual Inference &amp; Other Areas of Semantics </a><br/><span class="session-time" title="Wednesday, 6 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="56"><td><span class="poster-title">Tree-structured Decoding for Solving Math Word Problems. </span><em>Qianying Liu, Wenyv Guan, Sujian Li and Daisuke Kawahara</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-56" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="86"><td><span class="poster-title">PullNet: Open Domain Question Answering with Iterative Retrieval on Knowledge Bases and Text. </span><em>Haitian Sun, Tania Bedrax-Weiss and William Cohen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-86" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="107"><td><span class="poster-title">Cosmos QA: Machine Reading Comprehension with Contextual Commonsense Reasoning. </span><em>Lifu Huang, Ronan Le Bras, Chandra Bhagavatula and Yejin Choi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-107" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="179"><td><span class="poster-title">Finding Generalizable Evidence by Learning to Convince Q&A Models. </span><em>Ethan Perez, Siddharth Karamcheti, Rob Fergus, Jason Weston, Douwe Kiela and Kyunghyun Cho</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-179" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="468"><td><span class="poster-title">Ranking and Sampling in Open-Domain Question Answering. </span><em>Yanfu Xu, Zheng Lin, Yuanxin Liu, Rui Liu, Weiping Wang and Dan Meng</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-468" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="618"><td><span class="poster-title">A Non-commutative Bilinear Model for Answering Path Queries in Knowledge Graphs. </span><em>Katsuhiko Hayashi and Masashi Shimbo</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-618" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="807"><td><span class="poster-title">Generating Questions for Knowledge Bases via Incorporating Diversified Contexts and Answer-Aware Loss. </span><em>Cao Liu, Kang Liu, Shizhu He, Zaiqing Nie and Jun Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-807" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="924"><td><span class="poster-title">Multi-Task Learning for Conversational Question Answering over a Large-Scale Knowledge Base. </span><em>Tao Shen, Xiubo Geng, Tao QIN, Daya Guo, Duyu Tang, Nan Duan, Guodong Long and Daxin Jiang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-924" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1930"><td><span class="poster-title">BiPaR: A Bilingual Parallel Dataset for Multilingual and Cross-lingual Reading Comprehension on Novels. </span><em>Yimin Jing, Deyi Xiong and Zhen Yan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1930" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2085"><td><span class="poster-title">Language Models as Knowledge Bases?. </span><em>Fabio Petroni, Tim Rocktäschel, Sebastian Riedel, Patrick Lewis, Anton Bakhtin, Yuxiang Wu and Alexander Miller</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2085" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2237"><td><span class="poster-title">NumNet: Machine Reading Comprehension with Numerical Reasoning. </span><em>Qiu Ran, Yankai Lin, Peng Li, Jie Zhou and Zhiyuan Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2237" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2277"><td><span class="poster-title">Unicoder: A Universal Language Encoder by Pre-training with Multiple Cross-lingual Tasks. </span><em>Haoyang Huang, Yaobo Liang, Nan Duan, Ming Gong, Linjun Shou, Daxin Jiang and Ming Zhou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2277" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2390"><td><span class="poster-title">Addressing Semantic Drift in Question Generation for Semi-Supervised Question Answering. </span><em>Shiyue Zhang and Mohit Bansal</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2390" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2764"><td><span class="poster-title">Adversarial Domain Adaptation for Machine Reading Comprehension. </span><em>Huazheng Wang, Zhe Gan, Xiaodong Liu, Jingjing Liu, Jianfeng Gao and Hongning Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2764" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2820"><td><span class="poster-title">Incorporating External Knowledge into Machine Reading for Generative Question Answering. </span><em>Bin Bi, Chen Wu, Ming Yan, Wei Wang, Jiangnan Xia and Chenliang Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2820" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2825"><td><span class="poster-title">Answering questions by learning to rank - Learning to rank by answering questions. </span><em>George Sebastian Pirtoaca, Traian Rebedea and Stefan Ruseti</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2825" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2940"><td><span class="poster-title">Discourse-Aware Semantic Self-Attention for Narrative Reading Comprehension. </span><em>Todor Mihaylov and Anette Frank</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2940" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2945"><td><span class="poster-title">Revealing the Importance of Semantic Retrieval for Machine Reading at Scale. </span><em>Yixin Nie, Songhe Wang and Mohit Bansal</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2945" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2978"><td><span class="poster-title">PubMedQA: A Dataset for Biomedical Research Question Answering. </span><em>Qiao Jin, Bhuwan Dhingra, Zhengping Liu, William Cohen and Xinghua Lu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2978" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3164"><td><span class="poster-title">Quick and (not so) Dirty: Unsupervised Selection of Justification Sentences for Multi-hop Question Answering. </span><em>Vikas Yadav, Steven Bethard and Mihai Surdeanu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3164" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3417"><td><span class="poster-title">Answering Complex Open-domain Questions Through Iterative Query Generation. </span><em>Peng Qi, Xiaowen Lin, Leo Mehr, Zijian Wang and Christopher D. Manning</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3417" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3489"><td><span class="poster-title">NL2pSQL: Generating Pseudo-SQL Queries from Under-Specified Natural Language Questions. </span><em>Fuxiang Chen, Seung-won Hwang, Jaegul Choo, Jung-Woo Ha and Sunghun Kim</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3489" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4004"><td><span class="poster-title">Leveraging Frequent Query Substructures to Generate Formal Queries for Complex Question Answering. </span><em>Jiwei Ding, Wei Hu, Qixin Xu and Yuzhong Qu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4004" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="147"><td><span class="poster-title">Incorporating Graph Attention Mechanism into Knowledge Graph Reasoning Based on Deep Reinforcement Learning. </span><em>Heng Wang, Shuangyin Li, Rong Pan and Mingzhi Mao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-147" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="493"><td><span class="poster-title">Learning to Update Knowledge Graphs by Reading News. </span><em>Jizhi Tang, Yansong Feng and Dongyan Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-493" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="709"><td><span class="poster-title">DIVINE: A Generative Adversarial Imitation Learning Framework for Knowledge Graph Reasoning. </span><em>Ruiping Li and Xiang Cheng</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-709" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="829"><td><span class="poster-title">Original Semantics-Oriented Attention and Deep Fusion Network for Sentence Matching. </span><em>Mingtong Liu, Yujie Zhang, Jinan Xu and Yufeng Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-829" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="972"><td><span class="poster-title">Representation Learning with Ordered Relation Paths for Knowledge Graph Completion. </span><em>Yao Zhu, Hongzhi Liu, Zhonghai Wu, Yang Song and Tao Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-972" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1018"><td><span class="poster-title">Collaborative Policy Learning for Open Knowledge Graph Reasoning. </span><em>Cong Fu, Tong Chen, Meng Qu, Woojeong Jin and Xiang Ren</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1018" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1444"><td><span class="poster-title">Modeling Event Background for If-Then Commonsense Reasoning Using Context-aware Variational Autoencoder. </span><em>Li Du, Xiao Ding, Ting Liu and Zhongyang Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1444" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2257"><td><span class="poster-title">Asynchronous Deep Interaction Network for Natural Language Inference. </span><em>Di Liang, Fubao Zhang, Qi Zhang and Xuanjing Huang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2257" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2830"><td><span class="poster-title">Keep Calm and Switch On! Preserving Sentiment and Fluency in Semantic Text Exchange. </span><em>Steven Y. Feng, Aaron W. Li and Jesse Hoey</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2830" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3550"><td><span class="poster-title">Query-focused Scenario Construction. </span><em>Su Wang, Greg Durrett and Katrin Erk</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3550" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3819"><td><span class="poster-title">Semi-supervised Entity Alignment via Joint Knowledge Embedding Model and Cross-graph Model. </span><em>Chengjiang Li, Yixin Cao, Lei Hou, Jiaxin Shi, Juanzi Li and Tat-Seng Chua</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3819" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-57"><td><span class="poster-title">EUSP: An Easy-to-Use Semantic Parsing PlatForm. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-57" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-66"><td><span class="poster-title">ParaQG: A System for Generating Questions and Answers from Paragraphs. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-66" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-37"><td><span class="poster-title">CFO: A Framework for Building Production NLP Systems. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-37" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-48"><td><span class="poster-title">ABSApp: A Portable Weakly-Supervised Aspect-Based Sentiment Extraction System. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-48" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-86"><td><span class="poster-title">Memory Grounded Conversational Reasoning. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-86" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-lunch-4"><span class="session-title">Lunch</span><br/><span class="session-time" title="Wednesday, 6 November 2019">12:00 &ndash; 13:30</span></div>
<div class="session-box" id="session-box-6"><div class="session-header" id="session-header-6"> (Session 6)</div>
<div class="session session-expandable session-papers1" id="session-6a"><div id="expander"></div><a href="#" class="session-title">6A: Tagging, Chunking, Syntax &amp; Parsing</a><br/><span class="session-time" title="Wednesday, 6 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="4063"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Designing and Interpreting Probes with Control Tasks. </span><em>John Hewitt and Percy Liang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4063" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1357"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Specializing Word Embeddings (for Parsing) by Information Bottleneck. </span><em>Xiang Lisa Li and Jason Eisner</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1357" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2799"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Deep Contextualized Word Embeddings in Transition-Based and Graph-Based Dependency Parsing - A Tale of Two Parsers Revisited. </span><em>Artur Kulmizev, Miryam de Lhoneux, Johannes Gontrum, Elena Fano and Joakim Nivre</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2799" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2863"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Semantic graph parsing with recurrent neural network DAG grammars. </span><em>Federico Fancellu, Sorcha Gilroy, Adam Lopez and Mirella Lapata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2863" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1221"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">75 Languages, 1 Model: Parsing Universal Dependencies Universally. </span><em>Dan Kondratyuk and Milan Straka</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1221" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-6b"><div id="expander"></div><a href="#" class="session-title">6B: Question Answering II</a><br/><span class="session-time" title="Wednesday, 6 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1367"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Interactive Language Learning by Question Answering. </span><em>Xingdi Yuan, Marc-Alexandre Côté, Jie Fu, Zhouhan Lin, Chris Pal, Yoshua Bengio and Adam Trischler</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1367" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3238"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">What's Missing: A Knowledge Gap Guided Approach for Multi-hop Question Answering. </span><em>Tushar Khot, Ashish Sabharwal and Peter Clark</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3238" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="436"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">KagNet: Knowledge-Aware Graph Networks for Commonsense Reasoning. </span><em>Bill Yuchen Lin, Xinyue Chen, Jamin Chen and Xiang Ren</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-436" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3518"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Learning with Limited Data for Multilingual Reading Comprehension. </span><em>Kyungjae Lee, Sunghyun Park, Hojae Han, Jinyoung Yeo, Seung-won Hwang and Juho Lee</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3518" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3778"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">A Discrete Hard EM Approach for Weakly Supervised Question Answering. </span><em>Sewon Min, Danqi Chen, Hannaneh Hajishirzi and Luke Zettlemoyer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3778" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-6c"><div id="expander"></div><a href="#" class="session-title">6C: Linguistic Theories, Cognitive Modeling &amp; Psycholinguistics</a><br/><span class="session-time" title="Wednesday, 6 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2585"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Is the Red Square Big? MALeViC: Modeling Adjectives Leveraging Visual Contexts. </span><em>Sandro Pezzelle and Raquel Fernández</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2585" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3650"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Investigating BERT's Knowledge of Language: Five Analysis Methods with NPIs. </span><em>Alex Warstadt, Yu Cao, Ioana Grosu, Wei Peng, Hagen Blix, Yining Nie, Anna Alsop, Shikha Bordia, Haokun Liu, Alicia Parrish, Sheng-Fu Wang, Jason Phang, Anhad Mohananey, Phu Mon Htut, Paloma Jeretic and Samuel R. Bowman</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3650" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3929"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Representation of Constituents in Neural Language Models: Coordination Phrase as a Case Study. </span><em>Aixiu AN, Peng Qian, Ethan Wilcox and Roger Levy</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3929" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1745"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Towards Zero-shot Language Modeling. </span><em>Edoardo Maria Ponti, Ivan Vulić, Ryan Cotterell, Roi Reichart and Anna Korhonen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1745" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="TACL-1710"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Neural Network Acceptability Judgments. </span><em>Alex Warstadt, Amanpreet Singh and Samuel R. Bowman</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1710" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-6d"><div id="expander"></div><a href="#" class="session-title">6D: Sentiment Analysis &amp; Argument Mining II</a><br/><span class="session-time" title="Wednesday, 6 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-6d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-6d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2089"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">What Gets Echoed? Understanding the `Pointers` in Explanations of Persuasive Arguments. </span><em>David Atkinson, Kumar Bhargav Srinivasan and Chenhao Tan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2089" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2267"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Modeling Frames in Argumentation. </span><em>Yamen Ajjour, Milad Alshomary, Henning Wachsmuth and Benno Stein</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2267" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3321"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">AMPERSAND: Argument Mining for PERSuAsive oNline Discussions. </span><em>Tuhin Chakrabarty, Christopher Hidey, Smaranda Muresan, Kathy McKeown and Alyssa Hwang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3321" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="427"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Evaluating adversarial attacks against multiple fact verification systems. </span><em>James Thorne, Andreas Vlachos, Christos Christodoulopoulos and Arpit Mittal</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-427" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="564"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Nonsense!: Quality Control via Two-Step Reason Selection for Annotating Local Acceptability and Related Attributes in News Editorials. </span><em>Wonsuk Yang, seungwon yoon, Ada Carpenter and Jong Park</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-564" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-6"><div id="expander"></div><a href="#" class="session-title">6 Poster & Demo: Discourse &amp; Pragmatics, Summarization &amp; Generation </a><br/><span class="session-time" title="Wednesday, 6 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="723"><td><span class="poster-title">Evaluating Pronominal Anaphora in Machine Translation: An Evaluation Measure and a Test Suite. </span><em>Prathyusha Jwalapuram, Shafiq Joty, Irina Temnikova and Preslav Nakov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-723" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2916"><td><span class="poster-title">A Regularization Approach for Incorporating Event Knowledge and Coreference Relations into Neural Discourse Parsing. </span><em>Zeyu Dai and Ruihong Huang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2916" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3994"><td><span class="poster-title">Weakly Supervised Multilingual Causality Extraction from Wikipedia. </span><em>Chikara Hashimoto</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3994" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="210"><td><span class="poster-title">Attribute-aware Sequence Network for Review Summarization. </span><em>Junjie Li, Xuepeng Wang, Dawei Yin and Chengqing Zong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-210" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="268"><td><span class="poster-title">Extractive Summarization of Long Documents by Combining Global and Local Context. </span><em>Wen Xiao and Giuseppe Carenini</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-268" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="313"><td><span class="poster-title">Enhancing Neural Data-To-Text Generation Models with External Background Knowledge. </span><em>Shuang Chen, Jinpeng Wang, Xiaocheng Feng, Feng Jiang, Bing Qin and Chin-Yew Lin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-313" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="346"><td><span class="poster-title">Reading Like HER: Human Reading Inspired Extractive Summarization. </span><em>Ling Luo, Xiang Ao, Yan Song, Feiyang Pan, Min Yang and Qing He</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-346" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="361"><td><span class="poster-title">Contrastive Attention Mechanism for Abstractive Sentence Summarization. </span><em>Xiangyu Duan, Hongfei Yu, Mingming Yin, Min Zhang, Weihua Luo and Yue Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-361" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="703"><td><span class="poster-title">NCLS: Neural Cross-Lingual Summarization. </span><em>Junnan Zhu, Qian Wang, Yining Wang, Yu Zhou, Jiajun Zhang, Shaonan Wang and Chengqing Zong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-703" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="749"><td><span class="poster-title">Clickbait? Sensational Headline Generation with Auto-tuned Reinforcement Learning. </span><em>Peng Xu, Chien-Sheng Wu, Andrea Madotto and Pascale Fung</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-749" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="845"><td><span class="poster-title">Concept Pointer Network for Abstractive Summarization. </span><em>Wenbo Wang, Yang Gao, Heyan Huang and Yuxiang Zhou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-845" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1139"><td><span class="poster-title">Surface Realisation Using Full Delexicalisation. </span><em>Anastasia Shimorina and Claire Gardent</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1139" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1169"><td><span class="poster-title">IMaT: Unsupervised Text Attribute Transfer via Iterative Matching and Translation. </span><em>Zhijing Jin, Di Jin, Jonas Mueller, Nicholas Matthews and Enrico Santus</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1169" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1191"><td><span class="poster-title">Better Rewards Yield Better Summaries: Learning to Summarise Without References. </span><em>Florian Böhm, Yang Gao, Christian M. Meyer, Ori Shapira, Ido Dagan and Iryna Gurevych</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1191" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1369"><td><span class="poster-title">Mixture Content Selection for Diverse Sequence Generation. </span><em>Jaemin Cho, Minjoon Seo and Hannaneh Hajishirzi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1369" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1375"><td><span class="poster-title">An End-to-End Generative Architecture for Paraphrase Generation. </span><em>Qian Yang, zhouyuan huo, Dinghan Shen, Yong Cheng, Wenlin Wang, Guoyin Wang and Lawrence Carin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1375" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1726"><td><span class="poster-title">Table-to-Text Generation with Effective Hierarchical Encoder on Three Dimensions (Row, Column and Time). </span><em>Heng Gong, Xiaocheng Feng, Bing Qin and Ting Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1726" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1779"><td><span class="poster-title">Subtopic-driven Multi-Document Summarization. </span><em>Xin Zheng, Aixin Sun, Jing Li and Karthik Muthuswamy</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1779" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1805"><td><span class="poster-title">Referring Expression Generation Using Entity Profiles. </span><em>Meng Cao and Jackie Chi Kit Cheung</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1805" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1834"><td><span class="poster-title">Exploring Diverse Expressions for Paraphrase Generation. </span><em>Lihua Qian, Lin Qiu, Weinan Zhang, Xin Jiang and Yong Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1834" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1852"><td><span class="poster-title">Enhancing AMR-to-Text Generation with Dual Graph Representations. </span><em>Leonardo F. R. Ribeiro, Claire Gardent and Iryna Gurevych</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1852" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1881"><td><span class="poster-title">Keeping Consistency of Sentence Generation and Document Classification with Multi-Task Learning. </span><em>Toru Nishino, Shotaro Misawa, Ryuji Kano, Tomoki Taniguchi, Yasuhide Miura and Tomoko Ohkuma</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1881" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2031"><td><span class="poster-title">Toward a Task of Feedback Comment Generation for Writing Learning. </span><em>Ryo Nagata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2031" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2033"><td><span class="poster-title">Improving Question Generation With to the Point Context. </span><em>Jingjing Li, Yifan Gao, Lidong Bing, Irwin King and Michael R. Lyu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2033" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2121"><td><span class="poster-title">Deep Copycat Networks for Text-to-Text Generation. </span><em>Julia Ive, Pranava Madhyastha and Lucia Specia</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2121" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2412"><td><span class="poster-title">Towards Controllable and Personalized Review Generation. </span><em>Pan Li and Alexander Tuzhilin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2412" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2604"><td><span class="poster-title">Answers Unite! Unsupervised Metrics for Reinforced Summarization Models. </span><em>Thomas Scialom, Sylvain Lamprier, Benjamin Piwowarski and Jacopo Staiano</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2604" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2746"><td><span class="poster-title">Long and Diverse Text Generation with Planning-based Hierarchical Variational Model. </span><em>Zhihong Shao, Minlie Huang, Jiangtao Wen, Wenfei Xu and xiaoyan zhu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2746" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2932"><td><span class="poster-title">`Transforming` Delete, Retrieve, Generate Approach for Controlled Text Style Transfer. </span><em>Akhilesh Sudhakar, Bhargav Upadhyay and Arjun Maheswaran</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2932" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3275"><td><span class="poster-title">An Entity-Driven Framework for Abstractive Summarization. </span><em>Eva Sharma, Luyang Huang, Zhe Hu and Lu Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3275" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3334"><td><span class="poster-title">Neural Extractive Text Summarization with Syntactic Compression. </span><em>Jiacheng Xu and Greg Durrett</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3334" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3511"><td><span class="poster-title">Domain Adaptive Text Style Transfer. </span><em>Dianqi Li, Yizhe Zhang, Zhe Gan, Yu Cheng, Chris Brockett, Bill Dolan and Ming-Ting Sun</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3511" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3754"><td><span class="poster-title">Let's Ask Again: Refine Network for Automatic Question Generation. </span><em>Preksha Nema, Akash Kumar Mohankumar, Mitesh M. Khapra, Balaji Vasan Srinivasan and Balaraman Ravindran</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3754" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3846"><td><span class="poster-title">Earlier Isn't Always Better: Sub-aspect Analysis on Corpus and System Biases in Summarization. </span><em>Taehee Jung, Dongyeop Kang, Lucas Mentch and Eduard Hovy</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3846" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-5"><td><span class="poster-title">VizSeq: a visual analysis toolkit for text generation tasks. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-5" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-36"><td><span class="poster-title">FAMULUS: Interactive Annotation and Feedback Generation for Teaching Diagnostic Reasoning. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-36" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-74"><td><span class="poster-title">A Summarization System for Scientific Documents. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-74" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-94"><td><span class="poster-title">EASSE: Easier Automatic Sentence Simplification Evaluation. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-94" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-109"><td><span class="poster-title">ALTER: Auxiliary Text Rewriting Tool for Natural Language Generation. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-109" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-break-5"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Wednesday, 6 November 2019">15:00 &ndash; 15:30</span></div>
<div class="session-box" id="session-box-7"><div class="session-header" id="session-header-7"> (Session 7)</div>
<div class="session session-expandable session-papers1" id="session-7a"><div id="expander"></div><a href="#" class="session-title">7A: Machine Translation &amp; Multilinguality I</a><br/><span class="session-time" title="Wednesday, 6 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1131"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Lost in Evaluation: Misleading Benchmarks for Bilingual Dictionary Induction. </span><em>Yova Kementchedjhieva, Mareike Hartmann and Anders Søgaard</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1131" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1266"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Towards Realistic Practices In Low-Resource Natural Language Processing: The Development Set. </span><em>Katharina Kann, Kyunghyun Cho and Samuel R. Bowman</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1266" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1478"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Synchronously Generating Two Languages with Interactive Decoding. </span><em>Yining Wang, Jiajun Zhang, Long Zhou, Yuchen Liu and Chengqing Zong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1478" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1868"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">On NMT Search Errors and Model Errors: Cat Got Your Tongue?. </span><em>Felix Stahlberg and Bill Byrne</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1868" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-7b"><div id="expander"></div><a href="#" class="session-title">7B: Reasoning &amp; Question Answering</a><br/><span class="session-time" title="Wednesday, 6 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2533"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">`Going on a vacation` takes longer than `Going for a walk`: A Study of Temporal Commonsense Understanding. </span><em>Ben Zhou, Daniel Khashabi, Qiang Ning and Dan Roth</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2533" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2798"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">QAInfomax: Learning Robust Question Answering System by Mutual Information Maximization. </span><em>Yi-Ting Yeh and Yun-Nung Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2798" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="329"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Adapting Meta Knowledge Graph Information for Multi-Hop Reasoning over Few-Shot Relations. </span><em>Xin Lv, Yuxian Gu, Xu Han, Lei Hou, Juanzi Li and Zhiyuan Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-329" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="586"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">How Reasonable are Common-Sense Reasoning Tasks: A Case-Study on the Winograd Schema Challenge and SWAG. </span><em>Paul Trichelair, Ali Emami, Adam Trischler, Kaheer Suleman and Jackie Chi Kit Cheung</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-586" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-7c"><div id="expander"></div><a href="#" class="session-title">7C: Generation I</a><br/><span class="session-time" title="Wednesday, 6 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="267"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Pun-GAN: Generative Adversarial Network for Pun Generation. </span><em>Fuli Luo, Shunyao Li, Pengcheng Yang, Lei Li, Baobao Chang, Zhifang Sui and Xu SUN</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-267" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3820"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Multi-Task Learning with Language Modeling for Question Generation. </span><em>Wenjie Zhou, Minghua Zhang and Yunfang Wu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3820" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3506"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Autoregressive Text Generation Beyond Feedback Loops. </span><em>Florian Schmidt, Stephan Mandt and Thomas Hofmann</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3506" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3874"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">The Woman Worked as a Babysitter: On Biases in Language Generation. </span><em>Emily Sheng, Kai-Wei Chang, Premkumar Natarajan and Nanyun Peng</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3874" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-7d"><div id="expander"></div><a href="#" class="session-title">7D: Sentiment Analysis &amp; Argument Mining III</a><br/><span class="session-time" title="Wednesday, 6 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-7d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-7d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2984"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">On the Importance of Delexicalization for Fact Verification. </span><em>Sandeep Suntwal, Mithun Paul, Rebecca Sharp and Mihai Surdeanu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2984" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3338"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Towards Debiasing Fact Verification Models. </span><em>Tal Schuster, Darsh Shah, Yun Jie Serene Yeo, Daniel Roberto Filizzola Ortiz, Enrico Santus and Regina Barzilay</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3338" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="911"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Recognizing Conflict Opinions in Aspect-level Sentiment Classification with Dual Attention Networks. </span><em>Xingwei Tan, Yi Cai and Changxi Zhu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-911" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1395"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">Investigating Dynamic Routing in Tree-Structured LSTM for Sentiment Analysis. </span><em>Jin Wang, Liang-Chih Yu, K. Robert Lai and Xuejie Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1395" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-7"><div id="expander"></div><a href="#" class="session-title">7 Poster & Demo: Information Retrieval &amp; Document Analysis, Lexical Semantics, Sentence-level Semantics, Machine Learning </a><br/><span class="session-time" title="Wednesday, 6 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="542"><td><span class="poster-title">A Label Informative Wide & Deep Classifier for Patents and Papers. </span><em>Muyao Niu and Jie Cai</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-542" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="573"><td><span class="poster-title">Text Level Graph Neural Network for Text Classification. </span><em>Lianzhe Huang, Dehong Ma, Sujian Li, Xiaodong Zhang and Houfeng WANG</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-573" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="875"><td><span class="poster-title">Semantic Relatedness Based Re-ranker for Text Spotting. </span><em>Ahmed Sabir, Francesc Moreno and Lluís Padró</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-875" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1306"><td><span class="poster-title">Delta-training: Simple Semi-Supervised Text Classification using Pretrained Word Embeddings. </span><em>Hwiyeol Jo and Ceyda Cinarel</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1306" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1342"><td><span class="poster-title">Visual Detection with Context for Document Layout Analysis. </span><em>Carlos Soto and Shinjae Yoo</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1342" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1562"><td><span class="poster-title">Evaluating Topic Quality with Posterior Variability. </span><em>Linzi Xing, Michael J. Paul and Giuseppe Carenini</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1562" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2494"><td><span class="poster-title">Neural Topic Model with Reinforcement Learning. </span><em>Lin Gui, Jia Leng, Gabriele Pergola, yu zhou, Ruifeng Xu and Yulan He</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2494" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2705"><td><span class="poster-title">Modelling Stopping Criteria for Search Results using Poisson Processes. </span><em>Alison Sneyd and Mark Stevenson</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2705" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3533"><td><span class="poster-title">Cross-Domain Modeling of Sentence-Level Evidence for Document Retrieval. </span><em>Zeynep Akkalyoncu Yilmaz, Wei Yang, Haotian Zhang and Jimmy Lin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3533" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4151"><td><span class="poster-title">The Challenges of Optimizing Machine Translation for Low Resource Cross-Language Information Retrieval. </span><em>Constantine Lignos, Daniel Cohen, Yen-Chieh Lien, Pratik Mehta, W. Bruce Croft and Scott Miller</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4151" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="170"><td><span class="poster-title">Rotate King to get Queen: Word Relationships as Orthogonal Transformations in Embedding Space. </span><em>Kawin Ethayarajh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-170" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="362"><td><span class="poster-title">GlossBERT: BERT for Word Sense Disambiguation with Gloss Knowledge. </span><em>Luyao Huang, Chi Sun, Xipeng Qiu and Xuanjing Huang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-362" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="670"><td><span class="poster-title">Leveraging Adjective-Noun Phrasing Knowledge for Comparison Relation Prediction in Text-to-SQL. </span><em>Haoyan Liu, Lei Fang, Qian Liu, Bei Chen, Jian-Guang LOU and Zhoujun Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-670" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1461"><td><span class="poster-title">Bridging the Defined and the Defining: Exploiting Implicit Lexical Semantic Relations in Definition Modeling. </span><em>Koki Washio, Satoshi Sekine and Tsuneaki Kato</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1461" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1615"><td><span class="poster-title">Don't Just Scratch the Surface: Enhancing Word Representations for Korean with Hanja. </span><em>Kang Min Yoo, Taeuk Kim and Sang-goo Lee</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1615" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2219"><td><span class="poster-title">SyntagNet: Challenging Supervised Word Sense Disambiguation with Lexical-Semantic Combinations. </span><em>Marco Maru, Federico Scozzafava, Federico Martelli and Roberto Navigli</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2219" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2419"><td><span class="poster-title">Hierarchical Meta-Embeddings for Code-Switching Named Entity Recognition. </span><em>Genta Indra Winata, Zhaojiang Lin, Jamin Shin, Zihan Liu and Pascale Fung</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2419" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="327"><td><span class="poster-title">Fine-tune BERT with Sparse Self-Attention Mechanism. </span><em>Baiyun Cui, Yingming Li, Ming Chen and Zhongfei Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-327" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="806"><td><span class="poster-title">Feature-Dependent Confusion Matrices for Low-Resource NER Labeling with Noisy Labels. </span><em>Lukas Lange, Michael A. Hedderich and Dietrich Klakow</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-806" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="819"><td><span class="poster-title">A Multi-Pairwise Extension of Procrustes Analysis for Multilingual Word Translation. </span><em>Hagai Taitelbaum, Gal Chechik and Jacob Goldberger</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-819" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1063"><td><span class="poster-title">Out-of-Domain Detection for Low-Resource Text Classification Tasks. </span><em>Ming Tan, Yang Yu, Haoyu Wang, Dakuo Wang, Saloni Potdar, Shiyu Chang and Mo Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1063" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1877"><td><span class="poster-title">Harnessing Pre-Trained Neural Networks with Rules for Formality Style Transfer. </span><em>Yunli Wang, Yu Wu, Lili Mou, Zhoujun Li and Wenhan Chao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1877" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1925"><td><span class="poster-title">Multiple Text Style Transfer by using Word-level Conditional Generative Adversarial Network with Two-Phase Training. </span><em>Chih-Te Lai, Yi-Te Hong, Hong-You Chen, Chi-Jen Lu and Shou-De Lin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1925" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2104"><td><span class="poster-title">Improved Differentiable Architecture Search for Language Modeling and Named Entity Recognition. </span><em>Yufan Jiang, Chi Hu, Tong Xiao, Chunliang Zhang and Jingbo Zhu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2104" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2696"><td><span class="poster-title">Using Pairwise Occurrence Information to Improve Knowledge Graph Completion on Large-Scale Datasets. </span><em>Esma Balkir, Masha Naslidnyk, Dave Palfrey and Arpit Mittal</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2696" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2741"><td><span class="poster-title">Single Training Dimension Selection for Word Embedding with PCA. </span><em>Yu Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2741" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3040"><td><span class="poster-title">A Surprisingly Effective Fix for Deep Latent Variable Modeling of Text. </span><em>Bohan Li, Junxian He, Graham Neubig, Taylor Berg-Kirkpatrick and Yiming Yang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3040" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3115"><td><span class="poster-title">SciBERT: A Pretrained Language Model for Scientific Text. </span><em>Iz Beltagy, Kyle Lo and Arman Cohan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3115" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3265"><td><span class="poster-title">Humor Detection: A Transformer Gets the Last Laugh. </span><em>Orion Weller and Kevin Seppi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3265" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3585"><td><span class="poster-title">Combining Global Sparse Gradients with Local Gradients in Distributed Neural Network Training. </span><em>Alham Fikri Aji, Kenneth Heafield and Nikolay Bogoychev</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3585" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3631"><td><span class="poster-title">Small and Practical BERT Models for Sequence Labeling. </span><em>Henry Tsai, Jason Riesa, Melvin Johnson, Naveen Arivazhagan, Xin Li and Amelia Archer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3631" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3776"><td><span class="poster-title">Data Augmentation with Atomic Templates for Spoken Language Understanding. </span><em>Zijian Zhao, Su Zhu and Kai Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3776" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4026"><td><span class="poster-title">PaLM: A Hybrid Parser and Language Model. </span><em>Hao Peng, Roy Schwartz and Noah A. Smith</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4026" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1593"><td><span class="poster-title">A Pilot Study for Chinese SQL Semantic Parsing. </span><em>Qingkai Min, Yuefeng Shi and Yue Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1593" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1616"><td><span class="poster-title">Global Reasoning over Database Structures for Text-to-SQL Parsing. </span><em>Ben Bogin, Matt Gardner and Jonathan Berant</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1616" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1712"><td><span class="poster-title">Transductive Learning of Neural Language Models for Syntactic and Semantic Analysis. </span><em>Hiroki Ouchi, Jun Suzuki and Kentaro Inui</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1712" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2287"><td><span class="poster-title">Efficient Sentence Embedding using Discrete Cosine Transform. </span><em>Nada Almarwani, Hanan Aldarmaki and Mona Diab</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2287" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2393"><td><span class="poster-title">A Search-based Neural Model for Biomedical Nested and Overlapping Event Detection. </span><em>Kurt Junshean Espinosa, Makoto Miwa and Sophia Ananiadou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2393" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3233"><td><span class="poster-title">PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase Identification. </span><em>Yinfei Yang, Yuan Zhang, Chris Tar and Jason Baldridge</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3233" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3887"><td><span class="poster-title">Pretrained Language Models for Sequential Sentence Classification. </span><em>Arman Cohan, Iz Beltagy, Daniel King, Bhavana Dalvi and Dan Weld</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3887" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2402"><td><span class="poster-title">Emergent Linguistic Phenomena in Multi-Agent Communication Games. </span><em>Laura Harding Graesser, Kyunghyun Cho and Douwe Kiela</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2402" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1526"><td><span class="poster-title">TalkDown: A Corpus for Condescension Detection in Context. </span><em>Zijian Wang and Christopher Potts</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1526" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-break-6"><span class="session-title">Mini-Break</span><br/><span class="session-time" title="Wednesday, 6 November 2019">16:18 &ndash; 16:30</span></div>
<div class="session-box" id="session-box-8"><div class="session-header" id="session-header-8"> (Session 8)</div>
<div class="session session-expandable session-papers1" id="session-8a"><div id="expander"></div><a href="#" class="session-title">8A: Summarization</a><br/><span class="session-time" title="Wednesday, 6 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1178"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Summary Cloze: A New Task for Content Selection in Topic-Focused Summarization. </span><em>Daniel Deutsch and Dan Roth</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1178" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="392"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Text Summarization with Pretrained Encoders. </span><em>Yang Liu and Mirella Lapata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-392" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="609"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">How to Write Summaries with Patterns? Learning towards Abstractive Summarization through Prototype Editing. </span><em>Shen Gao, Xiuying Chen, Piji Li, Zhangming Chan, Dongyan Zhao and Rui Yan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-609" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3219"><td id="paper-time">17:24&ndash;17:42</td><td><span class="paper-title">BottleSum: Unsupervised and Self-supervised Sentence Summarization using the Information Bottleneck Principle. </span><em>Peter West, Ari Holtzman, Jan Buys and Yejin Choi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3219" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3043"><td id="paper-time">17:42&ndash;18:00</td><td><span class="paper-title">Improving Latent Alignment in Text Summarization by Generalizing the Pointer Generator. </span><em>Xiaoyu Shen, Yang Zhao, Hui Su and Dietrich Klakow</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3043" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-8b"><div id="expander"></div><a href="#" class="session-title">8B: Sentence-level Semantics II</a><br/><span class="session-time" title="Wednesday, 6 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2676"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Learning Semantic Parsers from Denotations with Latent Structured Alignments and Abstract Programs. </span><em>Bailin Wang, Ivan Titov and Mirella Lapata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2676" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="263"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Broad-Coverage Semantic Parsing as Transduction. </span><em>Sheng Zhang, Xutai Ma, Kevin Duh and Benjamin Van Durme</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-263" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1544"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Core Semantic First: A Top-down Approach for AMR Parsing. </span><em>Deng Cai and Wai Lam</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1544" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2904"><td id="paper-time">17:24&ndash;17:42</td><td><span class="paper-title">Don't paraphrase, detect! Rapid and Effective Data Collection for Semantic Parsing. </span><em>Jonathan Herzig and Jonathan Berant</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2904" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="TACL-1742"><td id="paper-time">17:42&ndash;18:00</td><td><span class="paper-title">Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond. </span><em>Mikel Artetxe and Holger Schwenk</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1742" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-8c"><div id="expander"></div><a href="#" class="session-title">8C: Information Extraction II</a><br/><span class="session-time" title="Wednesday, 6 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="337"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Improving Distantly-Supervised Relation Extraction with Joint Label Embedding. </span><em>Linmei Hu, Luhao Zhang, Chuan Shi, Liqiang Nie, Weili Guan and Cheng Yang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-337" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="566"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Leverage Lexical Knowledge for Chinese Named Entity Recognition via Collaborative Graph Network. </span><em>Dianbo Sui, Yubo Chen, Kang Liu, Jun Zhao and Shengping Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-566" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1057"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Looking Beyond Label Noise: Shifted Label Distribution Matters in Distantly Supervised Relation Extraction. </span><em>Qinyuan Ye, Liyuan Liu, Maosen Zhang and Xiang Ren</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1057" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1640"><td id="paper-time">17:24&ndash;17:42</td><td><span class="paper-title">Easy First Relation Extraction with Information Redundancy. </span><em>Shuai Ma, Gang Wang, Yansong Feng and Jinpeng Huai</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1640" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2509"><td id="paper-time">17:42&ndash;18:00</td><td><span class="paper-title">Dependency-Guided LSTM-CRF for Named Entity Recognition. </span><em>Zhanming Jie and Wei Lu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2509" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-8d"><div id="expander"></div><a href="#" class="session-title">8D: Information Retrieval &amp; Document Analysis I</a><br/><span class="session-time" title="Wednesday, 6 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-8d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-8d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1036"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Cross-Cultural Transfer Learning for Text Classification. </span><em>Dor Ringel, Gal Lavee, Ido Guy and Kira Radinsky</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1036" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1190"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Combining Unsupervised Pre-training and Annotator Rationales to Improve Low-shot Text Classification. </span><em>Oren Melamud, Mihaela Bornea and Ken Barker</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1190" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3202"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">ProSeqo: Projection Sequence Networks for On-Device Text Classification. </span><em>Zornitsa Kozareva and Sujith Ravi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3202" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3562"><td id="paper-time">17:24&ndash;17:42</td><td><span class="paper-title">Induction Networks for Few-Shot Text Classification. </span><em>Ruiying Geng, Binhua Li, Yongbin Li, Xiaodan Zhu, Ping Jian and Jian Sun</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3562" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2899"><td id="paper-time">17:42&ndash;18:00</td><td><span class="paper-title">Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach. </span><em>Wenpeng Yin, Jamaal Hay and Dan Roth</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2899" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-8"><div id="expander"></div><a href="#" class="session-title">8 Poster & Demo: Machine Learning </a><br/><span class="session-time" title="Wednesday, 6 November 2019">16:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="6"><td><span class="poster-title">A Logic-Driven Framework for Consistency of Neural Models. </span><em>Tao Li, Vivek Gupta, Maitrey Mehta and Vivek Srikumar</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-6" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="109"><td><span class="poster-title">Style Transfer for Texts: Retrain, Report Errors, Compare with Rewrites. </span><em>Alexey Tikhonov, Viacheslav Shibaev, Aleksander Nagaev, Aigul Nugmanova and Ivan P. Yamshchikov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-109" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="161"><td><span class="poster-title">Implicit Deep Latent Variable Models for Text Generation. </span><em>Le Fang, Chunyuan Li, Jianfeng Gao, Wen Dong and Changyou Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-161" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="200"><td><span class="poster-title">Text Emotion Distribution Learning from Small Sample: A Meta-Learning Approach. </span><em>Zhenjie Zhao and Xiaojuan Ma</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-200" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="247"><td><span class="poster-title">Judge the Judges: A Large-Scale Evaluation Study of Neural Language Models for Online Review Generation. </span><em>Cristina Garbacea, Samuel Carton, Shiyan Yan and Qiaozhu Mei</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-247" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="373"><td><span class="poster-title">Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. </span><em>Nils Reimers and Iryna Gurevych</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-373" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="399"><td><span class="poster-title">Learning Only from Relevant Keywords and Unlabeled Documents. </span><em>Nontawat Charoenphakdee, Jongyeong Lee, Yiping Jin, Dittaya Wanvarie and Masashi Sugiyama</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-399" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="592"><td><span class="poster-title">Denoising based Sequence-to-Sequence Pre-training for Text Generation. </span><em>Liang Wang, Wei Zhao, Ruoyu Jia, Sujian Li and Jingming Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-592" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="686"><td><span class="poster-title">Dialog Intent Induction with Deep Multi-View Clustering. </span><em>Hugh Perkins and Yi Yang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-686" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="718"><td><span class="poster-title">Nearly-Unsupervised Hashcode Representations for Biomedical Relation Extraction. </span><em>Sahil Garg, Aram Galstyan, Greg Ver Steeg and Guillermo Cecchi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-718" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="888"><td><span class="poster-title">Auditing Deep Learning processes through Kernel-based Explanatory Models. </span><em>Danilo Croce, Daniele Rossini and Roberto Basili</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-888" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1060"><td><span class="poster-title">Enhancing Variational Autoencoders with Mutual Information Neural Estimation for Text Generation. </span><em>Dong Qian and William K. Cheung</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1060" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1286"><td><span class="poster-title">Sampling Bias in Deep Active Classification: An Empirical Study. </span><em>Ameya Prabhu, Charles Dognin and Maneesh Singh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1286" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1321"><td><span class="poster-title">Don't Take the Easy Way Out: Ensemble Based Methods for Avoiding Known Dataset Biases. </span><em>Christopher Clark, Mark Yatskar and Luke Zettlemoyer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1321" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1360"><td><span class="poster-title">Achieving Verified Robustness to Symbol Substitutions via Interval Bound Propagation. </span><em>Po-Sen Huang, Robert Stanforth, Johannes Welbl, Chris Dyer, Dani Yogatama, Sven Gowal, Krishnamurthy Dvijotham and Pushmeet Kohli</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1360" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1422"><td><span class="poster-title">Rethinking Cooperative Rationalization: Introspective Extraction and Complement Control. </span><em>Mo Yu, Shiyu Chang, Yang Zhang and Tommi Jaakkola</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1422" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1435"><td><span class="poster-title">Experimenting with Power Divergences for Language Modeling. </span><em>Matthieu Labeau and Shay B. Cohen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1435" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1590"><td><span class="poster-title">Hierarchically-Refined Label Attention Network for Sequence Labeling. </span><em>Leyang Cui and Yue Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1590" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1709"><td><span class="poster-title">Certified Robustness to Adversarial Word Substitutions. </span><em>Robin Jia, Aditi Raghunathan, Kerem Göksel and Percy Liang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1709" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1846"><td><span class="poster-title">Visualizing and Understanding the Effectiveness of BERT. </span><em>Yaru Hao, Li Dong, Furu Wei and Ke Xu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1846" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2147"><td><span class="poster-title">Topics to Avoid: Demoting Latent Confounds in Text Classification. </span><em>Sachin Kumar, Shuly Wintner, Noah A. Smith and Yulia Tsvetkov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2147" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2168"><td><span class="poster-title">Learning to Ask for Conversational Machine Learning. </span><em>Shashank Srivastava, Igor Labutov and Tom Mitchell</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2168" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2270"><td><span class="poster-title">Language Modeling for Code-Switching: Evaluation, Integration of Monolingual Data, and Discriminative Training. </span><em>Hila Gonen and Yoav Goldberg</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2270" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2394"><td><span class="poster-title">Using Local Knowledge Graph Construction to Scale Seq2Seq Models to Multi-Document Inputs. </span><em>Angela Fan, Claire Gardent, Chloé Braud and Antoine Bordes</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2394" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2441"><td><span class="poster-title">Fine-grained Knowledge Fusion for Sequence Labeling Domain Adaptation. </span><em>Huiyun Yang, Shujian Huang, XIN-YU DAI and Jiajun CHEN</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2441" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2477"><td><span class="poster-title">Exploiting Monolingual Data at Scale for Neural Machine Translation. </span><em>Lijun Wu, Yiren Wang, Yingce Xia, Tao QIN, Jianhuang Lai and Tie-Yan Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2477" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2554"><td><span class="poster-title">Meta Relational Learning for Few-Shot Link Prediction in Knowledge Graphs. </span><em>Mingyang Chen, Wen Zhang, Wei Zhang, Qiang Chen and Huajun Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2554" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2660"><td><span class="poster-title">Distributionally Robust Language Modeling. </span><em>Yonatan Oren, Shiori Sagawa, Tatsunori Hashimoto and Percy Liang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2660" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2686"><td><span class="poster-title">Unsupervised Domain Adaptation of Contextualized Embeddings for Sequence Labeling. </span><em>Xiaochuang Han and Jacob Eisenstein</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2686" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2706"><td><span class="poster-title">Learning Latent Parameters without Human Response Patterns: Item Response Theory with Artificial Crowds. </span><em>John P. Lalor, Hao Wu and Hong Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2706" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2716"><td><span class="poster-title">Parallel Iterative Edit Models for Local Sequence Transduction. </span><em>Abhijeet Awasthi, Sunita Sarawagi, Rasna Goyal, Sabyasachi Ghosh and Vihari Piratla</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2716" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2882"><td><span class="poster-title">ARAML: A Stable Adversarial Training Framework for Text Generation. </span><em>Pei Ke, Fei Huang, Minlie Huang and xiaoyan zhu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2882" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2905"><td><span class="poster-title">FlowSeq:  Non-Autoregressive Conditional Sequence Generation with Generative Flow. </span><em>Xuezhe Ma, Chunting Zhou, Xian Li, Graham Neubig and Eduard Hovy</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2905" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3039"><td><span class="poster-title">Compositional Generalization for Primitive Substitutions. </span><em>Yuanpeng Li, Liang Zhao, Jianyu Wang and Joel Hestness</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3039" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3089"><td><span class="poster-title">WikiCREM: A Large Unsupervised Corpus for Coreference Resolution. </span><em>Vid Kocijan, Oana-Maria Camburu, Ana-Maria Cretu, Yordan Yordanov, Phil Blunsom and Thomas Lukasiewicz</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3089" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3146"><td><span class="poster-title">Identifying and Explaining Discriminative Attributes. </span><em>Armins Stepanjans and André Freitas</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3146" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3194"><td><span class="poster-title">Patient Knowledge Distillation for BERT Model Compression. </span><em>Siqi Sun, Yu Cheng, Zhe Gan and Jingjing Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3194" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3254"><td><span class="poster-title">Neural Gaussian Copula for Variational Autoencoder. </span><em>Prince Zizhuang Wang and William Yang Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3254" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3261"><td><span class="poster-title">Transformer Dissection: An Unified Understanding for Transformer's Attention via the Lens of Kernel. </span><em>Yao-Hung Hubert Tsai, Shaojie Bai, Makoto Yamada, Louis-Philippe Morency and Ruslan Salakhutdinov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3261" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3478"><td><span class="poster-title">Learning to Learn and Predict: A Meta-Learning Approach for Multi-Label Classification. </span><em>Jiawei Wu, Wenhan Xiong and William Yang Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3478" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3494"><td><span class="poster-title">Revealing the Dark Secrets of BERT. </span><em>Olga Kovaleva, Alexey Romanov, Anna Rogers and Anna Rumshisky</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3494" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4149"><td><span class="poster-title">Machine Translation With Weakly Paired Documents. </span><em>Lijun Wu, Jinhua Zhu, Di He, Fei Gao, Tao QIN, Jianhuang Lai and Tie-Yan Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4149" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2201"><td><span class="poster-title">Countering Language Drift via Visual Grounding. </span><em>Jason Lee, Kyunghyun Cho and Douwe Kiela</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2201" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2415"><td><span class="poster-title">The Bottom-up Evolution of Representations in the Transformer: A Study with Machine Translation and Language Modeling Objectives. </span><em>Elena Voita, Rico Sennrich and Ivan Titov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2415" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-41"><td><span class="poster-title">NeuronBlocks: Building Your NLP DNN Models Like Playing Lego. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-41" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-42"><td><span class="poster-title">Controlling Sequence-to-Sequence Models - A Demonstration on Neural-based Acrostic Generator. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-42" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-44"><td><span class="poster-title">AllenNLP Interpret: A Framework for Explaining Predictions of NLP Models. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-44" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-54"><td><span class="poster-title">UER: An Open-Source Toolkit for Pre-training Models. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-54" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-85"><td><span class="poster-title">MedCATTrainer: A Biomedical Free Text Annotation Interface with Active Learning and Research Use Case Specific Customisation. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-85" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="day" id="day-5">Thursday, 7 November 2019</div>
<div class="session session-expandable session-plenary"><div id="expander"></div><a href="#" class="session-title"><strong>Keynote III: "Curiosity-driven Journey into Neural Sequence Models"</strong></a><br/><span class="session-people"><a href="http://www.kyunghyuncho.me" target="_blank">Kyunghyun Cho (New York University)</a></span><br/><span class="session-time" title="Thursday, 7 November 2019">09:00 &ndash; 10:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><div class="paper-session-details"><br/><div class="session-abstract"><p>In this talk, I take the audience on a tour of my earlier and recent experiences in building neural sequence models. I start from the earlier experience of using a recurrent net for sequence-to-sequence learning and talk about the attention mechanism. I discuss factors behind the success of these earlier approaches, and how these were embraced by the community even before they sota’d. I then move on to more recent research direction in unconventional neural sequence models that automatically learn to decide on the order of generation.</p></div></div></div>
<div class="session session-break session-plenary" id="session-break-7"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Thursday, 7 November 2019">10:00 &ndash; 10:30</span></div>
<div class="session-box" id="session-box-9"><div class="session-header" id="session-header-9"> (Session 9)</div>
<div class="session session-expandable session-papers1" id="session-9a"><div id="expander"></div><a href="#" class="session-title">9A: Machine Translation &amp; Multilinguality II</a><br/><span class="session-time" title="Thursday, 7 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2459"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Do We Really Need Fully Unsupervised Cross-Lingual Embeddings?. </span><em>Ivan Vulić, Goran Glavaš, Roi Reichart and Anna Korhonen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2459" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2491"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Weakly-Supervised Concept-based Adversarial Learning for Cross-lingual Word Embeddings. </span><em>Haozhou Wang, James Henderson and Paola Merlo</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2491" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3541"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Aligning Cross-Lingual Entities with Multi-Aspect Information. </span><em>Hsiu-Wei Yang, Yanyan Zou, Peng Shi, Wei Lu, Jimmy Lin and Xu SUN</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3541" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2498"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Contrastive Language Adaptation for Cross-Lingual Stance Detection. </span><em>Mitra Mohtarami, James Glass and Preslav Nakov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2498" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="422"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Jointly Learning to Align and Translate with Transformer Models. </span><em>Sarthak Garg, Stephan Peitz, Udhyakumar Nallasamy and Matthias Paulik</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-422" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-9b"><div id="expander"></div><a href="#" class="session-title">9B: Reasoning</a><br/><span class="session-time" title="Thursday, 7 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1334"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Social IQa: Commonsense Reasoning about Social Interactions. </span><em>Maarten Sap, Hannah Rashkin, Derek Chen, Ronan Le Bras and Yejin Choi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1334" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2866"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Self-Assembling Modular Networks for Interpretable Multi-Hop Reasoning. </span><em>Yichen Jiang and Mohit Bansal</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2866" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1413"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Posing Fair Generalization Tasks for Natural Language Inference. </span><em>Atticus Geiger, Ignacio Cases, Lauri Karttunen and Christopher Potts</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1413" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3279"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">Everything Happens for a Reason: Discovering the Purpose of Actions in Procedural Text. </span><em>Bhavana Dalvi, Niket Tandon, Antoine Bosselut, Wen-tau Yih and Peter Clark</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3279" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3183"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">CLUTRR: A Diagnostic Benchmark for Inductive Reasoning from Text. </span><em>Koustuv Sinha, Shagun Sodhani, Jin Dong, Joelle Pineau and William L. Hamilton</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3183" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-9c"><div id="expander"></div><a href="#" class="session-title">9C: Dialog &amp; Interactive Systems II</a><br/><span class="session-time" title="Thursday, 7 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="510"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Taskmaster-1: Toward a Realistic and Diverse Dialog Dataset. </span><em>Bill Byrne, Karthik Krishnamoorthi, Chinnadhurai Sankar, Arvind Neelakantan, Ben Goodrich, Daniel Duckworth, Semih Yavuz, Amit Dubey, Kyu-Young Kim and Andy Cedilnik</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-510" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1564"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Multi-Domain Goal-Oriented Dialogues (MultiDoGO): Strategies toward Curating and Annotating Large Scale Dialogue Data. </span><em>Denis Peskov, Nancy Clarke, Jason Krone, Brigi Fodor, Yi Zhang, Adel Youssef and Mona Diab</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1564" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1186"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Build it Break it Fix it for Dialogue Safety: Robustness from Adversarial Human Attack. </span><em>Emily Dinan, Samuel Humeau, Bharath Chintagunta and Jason Weston</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1186" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1853"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">GECOR: An End-to-End Generative Ellipsis and Co-reference Resolution Model for Task-Oriented Dialogue. </span><em>Jun Quan, Deyi Xiong, Bonnie Webber and Changjian Hu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1853" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="496"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Task-Oriented Conversation Generation Using Heterogeneous Memory Networks. </span><em>Zehao Lin, Xinjing Huang, Feng Ji, Haiqing Chen and Yin Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-496" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-9d"><div id="expander"></div><a href="#" class="session-title">9D: Sentiment Analysis &amp; Argument Mining IV</a><br/><span class="session-time" title="Thursday, 7 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-9d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-9d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="381"><td id="paper-time">10:30&ndash;10:48</td><td><span class="paper-title">Aspect-based Sentiment Classification with Aspect-specific Graph Convolutional Networks. </span><em>Chen Zhang, Qiuchi Li and Dawei Song</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-381" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1988"><td id="paper-time">10:48&ndash;11:06</td><td><span class="paper-title">Coupling Global and Local Context for Unsupervised Aspect Extraction. </span><em>Ming Liao, Jing Li, Haisong Zhang, Lingzhi Wang, Xixin Wu and Kam-Fai Wong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1988" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="65"><td id="paper-time">11:06&ndash;11:24</td><td><span class="paper-title">Transferable End-to-End Aspect-based Sentiment Analysis with Selective Adversarial Learning. </span><em>Zheng Li, Xin Li, Ying Wei, Lidong Bing, Yu Zhang and Qiang Yang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-65" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1995"><td id="paper-time">11:24&ndash;11:42</td><td><span class="paper-title">CAN: Constrained Attention Networks for Multi-Aspect Sentiment Analysis. </span><em>Mengting Hu, Shiwan Zhao, Li Zhang, Keke Cai, Zhong Su, Renhong Cheng and Xiaowei Shen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1995" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3207"><td id="paper-time">11:42&ndash;12:00</td><td><span class="paper-title">Leveraging Just a Few Keywords for Fine-Grained Aspect Detection Through Weakly Supervised Co-Training. </span><em>Giannis Karamanolakis, Daniel Hsu and Luis Gravano</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3207" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-9"><div id="expander"></div><a href="#" class="session-title">9 Poster & Demo: Social Media &amp; Computational Social Science, Text Mining &amp; NLP Applications </a><br/><span class="session-time" title="Thursday, 7 November 2019">10:30 &ndash; 12:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="52"><td><span class="poster-title">Integrating Text and Image: Determining Multimodal Document Intent in Instagram Posts. </span><em>Julia Kruk, Jonah Lubin, Karan Sikka, Xiao Lin, Dan Jurafsky and Ajay Divakaran</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-52" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="705"><td><span class="poster-title">Neural Conversation Recommendation with Online Interaction Modeling. </span><em>Xingshan Zeng, Jing Li, Lu Wang and Kam-Fai Wong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-705" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="720"><td><span class="poster-title">Different Absorption from the Same Sharing: Sifted Multi-task Learning for Fake News Detection. </span><em>Lianwei Wu, Yuan Rao, Haolin Jin, Ambreen Nazir and Ling Sun</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-720" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="965"><td><span class="poster-title">Text-based inference of moral sentiment change. </span><em>Jing Yi Xie, Renato Ferreira Pinto Junior, Graeme Hirst and Yang Xu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-965" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1439"><td><span class="poster-title">Detecting Causal Language Use in Science Findings. </span><em>Bei Yu, Yingya Li and Jun Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1439" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1468"><td><span class="poster-title">Multilingual and Multi-Aspect Hate Speech Analysis. </span><em>Nedjma Ousidhoum, Zizheng Lin, Hongming Zhang, Yangqiu Song and Dit-Yan Yeung</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1468" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1969"><td><span class="poster-title">MultiFC: A Real-World Multi-Domain Dataset for Evidence-Based Fact Checking of Claims. </span><em>Isabelle Augenstein, Christina Lioma, Dongsheng Wang, Lucas Chaves Lima, Casper Hansen, Christian Hansen and Jakob Grue Simonsen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1969" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2006"><td><span class="poster-title">A Deep Neural Information Fusion Architecture for Textual Network Embeddings. </span><em>Zenan Xu, Qinliang Su, Xiaojun Quan and Weijia Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2006" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2186"><td><span class="poster-title">You Shall Know a User by the Company It Keeps: Dynamic Representations for Social Media Users in NLP. </span><em>Marco Del Tredici, Diego Marcheggiani, Sabine Schulte im Walde and Raquel Fernández</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2186" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2606"><td><span class="poster-title">Adaptive Ensembling: Unsupervised Domain Adaptation for Political Document Analysis. </span><em>Shrey Desai, Barea Sinno, Alex Rosenfeld and Junyi Jessy Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2606" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2659"><td><span class="poster-title">Macrocosm: Social Media Persona Linking for Open Source Intelligence Applications. </span><em>Graham Horwood, Ning Yu, Thomas Boggs, Changjiang Yang and Chad Holvenstot</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2659" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2693"><td><span class="poster-title">A Hierarchical Location Prediction Neural Network for Twitter User Geolocation. </span><em>Binxuan Huang and Kathleen Carley</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2693" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2828"><td><span class="poster-title">Trouble on the Horizon: Forecasting the Derailment of Online Conversations as they Develop. </span><em>Jonathan P. Chang and Cristian Danescu-Niculescu-Mizil</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2828" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3391"><td><span class="poster-title">A Benchmark Dataset for Learning to Intervene in Online Hate Speech. </span><em>Jing Qian, Anna Bethke, Yinyin Liu, Elizabeth Belding and William Yang Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3391" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3461"><td><span class="poster-title">Detecting and Reducing Bias in a High Stakes Domain. </span><em>Ruiqi Zhong, Yanda Chen, Desmond Patton, Charlotte Selous and Kathy McKeown</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3461" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3566"><td><span class="poster-title">CodeSwitch-Reddit: Exploration of Written Multilingual Discourse in Online Discussion Forums. </span><em>Ella Rabinovich, Masih Sultani and Suzanne Stevenson</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3566" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3592"><td><span class="poster-title">Modeling Conversation Structure and Temporal Dynamics for Jointly Predicting Rumor Stance and Veracity. </span><em>Penghui Wei, Nan Xu and Wenji Mao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3592" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="TACL-1639"><td><span class="poster-title">Measuring Online Debaters' Persuasive Skill from Text over Time. </span><em>Kelvin Luu, Chenhao Tan and Noah A. Smith</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1639" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="142"><td><span class="poster-title">Reconstructing Capsule Networks for Zero-shot Intent Classification. </span><em>Han Liu, Xiaotong Zhang, Lu Fan, Xuandi Fu, Qimai Li, Xiao-Ming Wu and Albert Y.S. Lam</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-142" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="239"><td><span class="poster-title">Domain Adaptation for Person-Job Fit with Transferable Deep Global Match Network. </span><em>Shuqing Bian, Wayne Xin Zhao, Yang Song, Tao Zhang and Ji-Rong Wen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-239" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="299"><td><span class="poster-title">Heterogeneous Graph Attention Networks for Semi-supervised Short Text Classification. </span><em>Hu Linmei, Tianchi Yang, Chuan Shi, Houye Ji and Xiaoli Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-299" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="438"><td><span class="poster-title">Comparing and Developing Tools to Measure the Readability of Domain-Specific Texts. </span><em>Elissa Redmiles, Lisa Maszkiewicz, Emily Hwang, Dhruv Kuchhal, Everest Liu, Miraida Morales, Denis Peskov, Sudha Rao, Rock Stevens, Kristina Gligorić, Sean Kross, Michelle Mazurek and Hal Daumé III</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-438" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="473"><td><span class="poster-title">News2vec: News Network Embedding with Subnode Information. </span><em>Ye Ma, Lu Zong, Yikang Yang and Jionglong Su</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-473" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="732"><td><span class="poster-title">Recursive Context-Aware Lexical Simplification. </span><em>Sian Gooding and Ekaterina Kochmar</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-732" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1103"><td><span class="poster-title">Leveraging Medical Literature for Section Prediction in Electronic Health Records. </span><em>Sara Rosenthal, Ken Barker and Zhicheng Liang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1103" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1459"><td><span class="poster-title">Neural News Recommendation with Heterogeneous User Behavior. </span><em>Chuhan Wu, Fangzhao Wu, Mingxiao An, Tao Qi, Jianqiang Huang, Yongfeng Huang and Xing Xie</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1459" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1470"><td><span class="poster-title">Reviews Meet Graphs: Enhancing User and Item Representations for Recommendation with Hierarchical Attentive Graph Neural Network. </span><em>Chuhan Wu, Fangzhao Wu, Tao Qi, Suyu Ge, Yongfeng Huang and Xing Xie</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1470" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1551"><td><span class="poster-title">Event Representation Learning Enhanced with External Commonsense Knowledge. </span><em>Xiao Ding, Kuo Liao, Ting Liu, Zhongyang Li and Junwen Duan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1551" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1572"><td><span class="poster-title">Learning to Discriminate Perturbations for Blocking Adversarial Attacks in Text Classification. </span><em>Yichao Zhou, Jyun-Yu Jiang, Kai-Wei Chang and Wei Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1572" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1661"><td><span class="poster-title">A Neural Citation Count Prediction Model based on Peer Review Text. </span><em>Siqing Li, Wayne Xin Zhao, Eddy Jing Yin and Ji-Rong Wen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1661" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2044"><td><span class="poster-title">Connecting the Dots: Document-level Neural Relation Extraction with Edge-oriented Graphs. </span><em>Fenia Christopoulou, Makoto Miwa and Sophia Ananiadou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2044" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2052"><td><span class="poster-title">Semi-supervised Text Style Transfer: Cross Projection in Latent Space. </span><em>Mingyue Shang, Piji Li, Zhenxin Fu, Lidong Bing, Dongyan Zhao, Shuming Shi and Rui Yan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2052" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2129"><td><span class="poster-title">Question Answering for Privacy Policies: Combining Computational and Legal Perspectives. </span><em>Abhilasha Ravichander, Alan W Black, Shomir Wilson, Thomas Norton and Norman Sadeh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2129" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2381"><td><span class="poster-title">Stick to the Facts: Learning towards a Fidelity-oriented E-Commerce Product Description Generation. </span><em>Zhangming Chan, Xiuying Chen, Yongliang Wang, Juntao Li, Zhiqiang Zhang, Kun Gai, Dongyan Zhao and Rui Yan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2381" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2389"><td><span class="poster-title">Fine-Grained Entity Typing via Hierarchical Multi Graph Convolutional Networks. </span><em>Hailong Jin, Lei Hou, Juanzi Li and Tiansi Dong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2389" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2942"><td><span class="poster-title">Learning to Infer Entities, Properties and their Relations from Clinical Conversations. </span><em>Nan Du, Mingqiu Wang, Linh Tran, Gang Lee and Izhak Shafran</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2942" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3072"><td><span class="poster-title">Practical Correlated Topic Modeling and Analysis via the Rectified Anchor Word Algorithm. </span><em>Moontae Lee, Sungjun Cho, David Bindel and David Mimno</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3072" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3128"><td><span class="poster-title">Modeling the Relationship between User Comments and Edits in Document Revision. </span><em>Xuchao Zhang, Dheeraj Rajagopal, Michael Gamon, Sujay Kumar Jauhar and ChangTien Lu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3128" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3218"><td><span class="poster-title">PRADO: Projection Attention Networks for Document Classification On-Device. </span><em>Prabhu Kaliamoorthi, Sujith Ravi and Zornitsa Kozareva</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3218" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3873"><td><span class="poster-title">Subword Language Model for Query Auto-Completion. </span><em>Gyuwan Kim</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3873" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4069"><td><span class="poster-title">Enhancing Dialogue Symptom Diagnosis with Global Attention and Symptom Graph. </span><em>Xinzhu Lin, Xiahui He, Qin Chen, Huaixiao Tou, Zhongyu Wei and Ting Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4069" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-39"><td><span class="poster-title">TEASPN: Framework and Protocol for Integrated Writing Assistance Environments. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-39" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-89"><td><span class="poster-title">Journalist-in-the-Loop: Continuous Learning as a Service for Rumour Analysis. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-89" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-98"><td><span class="poster-title">MAssistant: A Personal Knowledge Assistant for MOOC Learners. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-98" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-105"><td><span class="poster-title">A Stylometry Toolkit for Latin Literature. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-105" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-114"><td><span class="poster-title">Tanbih: Get To Know What You Are Reading. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-114" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="DEMO-112"><td><span class="poster-title">Visualizing Trends of Key Roles in News Articles. </span><em>TODO</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-DEMO-112" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-lunch-5"><span class="session-title">Lunch</span><br/><span class="session-time" title="Thursday, 7 November 2019">12:00 &ndash; 12:30</span></div>
<div class="session session-expandable session-plenary" id="session-business"><div id="expander"></div><a href="#" class="session-title">SIGDAT Business Meeting</a><br/><span class="session-time" title="Thursday, 7 November 2019">12:30 &ndash; 13:30</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"> <br/><div class="session-abstract">All attendees are encouraged to participate in the business meeting.</div></div></div>
<div class="session-box" id="session-box-10"><div class="session-header" id="session-header-10"> (Session 10)</div>
<div class="session session-expandable session-papers1" id="session-10a"><div id="expander"></div><a href="#" class="session-title">10A: Generation II</a><br/><span class="session-time" title="Thursday, 7 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-10a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-10a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3328"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Counterfactual Story Reasoning and Generation. </span><em>Lianhui Qin, Antoine Bosselut, Ari Holtzman, Chandra Bhagavatula, Elizabeth Clark and Yejin Choi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3328" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2395"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Encode, Tag, Realize: High-Precision Text Editing. </span><em>Eric Malmi, Sebastian Krause, Sascha Rothe, Daniil Mirylenka and Aliaksei Severyn</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2395" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="128"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Answer-guided and Semantic Coherent Question Generation in Open-domain Conversation. </span><em>Weichao Wang, Shi Feng, Daling Wang and Yifei Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-128" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1947"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Read, Attend and Comment: A Deep Architecture for Automatic News Comment Generation. </span><em>Ze Yang, Can Xu, wei wu and zhoujun li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1947" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2822"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">A Topic Augmented Text Generation Model: Joint Learning of Semantics and Structural Features. </span><em>hongyin tang, Miao Li and Beihong Jin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2822" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-10b"><div id="expander"></div><a href="#" class="session-title">10B: Speech, Vision, Robotics, Multimodal &amp; Grounding II</a><br/><span class="session-time" title="Thursday, 7 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-10b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-10b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3048"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">LXMERT: Learning Cross-Modality Encoder Representations from Transformers. </span><em>Hao Tan and Mohit Bansal</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3048" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3765"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">Phrase Grounding by Soft-Label Chain Conditional Random Field. </span><em>Jiacheng Liu and Julia Hockenmaier</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3765" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="549"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">What You See is What You Get: Visual Pronoun Coreference Resolution in Dialogues. </span><em>Xintong Yu, Hongming Zhang, Yangqiu Song, Yan Song and Changshui Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-549" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="122"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">YouMakeup: A Large-Scale Domain-Specific Multimodal Dataset for Fine-Grained Semantic Comprehension. </span><em>Weiying Wang, Yongcheng Wang, Shizhe Chen and Qin Jin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-122" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="167"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">DEBUG: A Dense Bottom-Up Grounding Approach for Natural Language Video Localization. </span><em>Chujie Lu, Long Chen, Chilie Tan, Xiaolin Li and Jun Xiao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-167" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-10c"><div id="expander"></div><a href="#" class="session-title">10C: Information Extraction III</a><br/><span class="session-time" title="Thursday, 7 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-10c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-10c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2712"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">CrossWeigh: Training Named Entity Tagger from Imperfect Annotations. </span><em>Zihan Wang, Jingbo Shang, Liyuan Liu, Lihao Lu, Jiacheng Liu and Jiawei Han</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2712" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3259"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">A Little Annotation does a Lot of Good: A Study in Bootstrapping Low-resource Named Entity Recognizers. </span><em>Aditi Chaudhary, Jiateng Xie, Zaid Sheikh, Graham Neubig and Jaime Carbonell</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3259" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1119"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Open Domain Web Keyphrase Extraction Beyond Language Modeling. </span><em>Lee Xiong, Chuan Hu, Chenyan Xiong, Daniel Campos and Arnold Overwijk</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1119" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="990"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">TuckER: Tensor Factorization for Knowledge Graph Completion. </span><em>Ivana Balazevic, Carl Allen and Timothy Hospedales</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-990" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="TACL-1712"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">Weakly Supervised Domain Detection. </span><em>Yumo Xu and Mirella Lapata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1712" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-10d"><div id="expander"></div><a href="#" class="session-title">10D: Information Retrieval &amp; Document Analysis II</a><br/><span class="session-time" title="Thursday, 7 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-10d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-10d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="425"><td id="paper-time">13:30&ndash;13:48</td><td><span class="paper-title">Human-grounded Evaluations of Explanation Methods for Text Classification. </span><em>Piyawat Lertvittayakumjorn and Francesca Toni</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-425" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="793"><td id="paper-time">13:48&ndash;14:06</td><td><span class="paper-title">A Context-based Framework for Modeling the Role and Function of On-line Resource Citations in Scientific Literature. </span><em>He Zhao, Zhunchen Luo, Chong Feng, Anqing Zheng and Xiaopeng Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-793" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="28"><td id="paper-time">14:06&ndash;14:24</td><td><span class="paper-title">Adversarial Reprogramming of Text Classification Neural Networks. </span><em>Paarth Neekhara, Shehzeen Hussain, Shlomo Dubnov and Farinaz Koushanfar</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-28" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1676"><td id="paper-time">14:24&ndash;14:42</td><td><span class="paper-title">Document Hashing with Mixture-Prior Generative Models. </span><em>Wei Dong, Qinliang Su, Dinghan Shen and Changyou Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1676" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3421"><td id="paper-time">14:42&ndash;15:00</td><td><span class="paper-title">On Efficient Retrieval of Top Similarity Vectors. </span><em>Shulong Tan, Zhixin Zhou, Zhaozhuo Xu and Ping Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3421" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-10"><div id="expander"></div><a href="#" class="session-title">10 Poster & Demo: Sentiment Analysis &amp; Argument Mining, Lexical Semantics, Sentence-level Semantics </a><br/><span class="session-time" title="Thursday, 7 November 2019">13:30 &ndash; 15:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="623"><td><span class="poster-title">Multiplex Word Embeddings for Selectional Preference Acquisition. </span><em>Hongming Zhang, Jiaxin Bai, Yan Song, Kun Xu, Changlong Yu, Yangqiu Song, Wilfred Ng and Dong Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-623" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="700"><td><span class="poster-title">MulCode: A Multiplicative Multi-way Model for Compressing Neural Language Model. </span><em>Yukun Ma, Patrick H. Chen and Cho-Jui Hsieh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-700" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1220"><td><span class="poster-title">It's All in the Name: Mitigating Gender Bias with Name-Based Counterfactual Data Substitution. </span><em>Rowan Hall Maudslay, Hila Gonen, Ryan Cotterell and Simone Teufel</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1220" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1741"><td><span class="poster-title">Examining Gender Bias in Languages with Grammatical Gender. </span><em>Pei Zhou, Weijia Shi, Jieyu Zhao, Kuan-Hao Huang, Muhao Chen, Ryan Cotterell and Kai-Wei Chang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1741" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3071"><td><span class="poster-title">Weakly Supervised Cross-lingual Semantic Relation Classification via Knowledge Distillation. </span><em>Yogarshi Vyas and Marine Carpuat</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3071" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3702"><td><span class="poster-title">Improved Word Sense Disambiguation Using Pre-Trained Contextualized Word Representations. </span><em>Christian Hadiwinoto, Hwee Tou Ng and Wee Chung Gan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3702" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3972"><td><span class="poster-title">Do NLP Models Know Numbers? Probing Numeracy in Embeddings. </span><em>Eric Wallace, Yizhong Wang, Sujian Li, Sameer Singh and Matt Gardner</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3972" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="552"><td><span class="poster-title">A Split-and-Recombine Approach for Follow-up Query Analysis. </span><em>Qian Liu, Bei Chen, Haoyan Liu, Jian-Guang LOU, Lei Fang, Bin Zhou and Dongmei Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-552" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1086"><td><span class="poster-title">Text2Math: End-to-end Parsing Text into Math Expressions. </span><em>Yanyan Zou and Wei Lu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1086" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1287"><td><span class="poster-title">Editing-Based SQL Query Generation for Cross-Domain Context-Dependent Questions. </span><em>Rui Zhang, Tao Yu, Heyang Er, Sungrok Shim, Eric Xue, Xi Victoria Lin, Tianze Shi, Caiming Xiong, Richard Socher and Dragomir Radev</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1287" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1351"><td><span class="poster-title">Syntax-aware Multilingual Semantic Role Labeling. </span><em>Shexia He, Zuchao Li and Hai Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1351" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1446"><td><span class="poster-title">Cloze-driven Pretraining of Self-attention Networks. </span><em>Alexei Baevski, Sergey Edunov, Yinhan Liu, Luke Zettlemoyer and Michael Auli</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1446" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1558"><td><span class="poster-title">Bridging the Gap between Relevance Matching and Semantic Matching for Short Text Similarity Modeling. </span><em>Jinfeng Rao, Linqing Liu, Yi Tay, Wei Yang, Peng Shi and Jimmy Lin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1558" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1836"><td><span class="poster-title">A Syntax-aware Multi-task Learning Framework for Chinese Semantic Role Labeling. </span><em>Qingrong Xia, Zhenghua Li and Min Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1836" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2060"><td><span class="poster-title">Transfer Fine-Tuning: A BERT Case Study. </span><em>Yuki Arase and Jun'ichi Tsujii</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2060" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2231"><td><span class="poster-title">Data-Anonymous Encoding for Text-to-SQL Generation. </span><em>Zhen Dong, Shizhao Sun, Hongzhi Liu, Jian-Guang Lou and Dongmei Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2231" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2993"><td><span class="poster-title">Capturing Argument Interaction in Semantic Role Labeling with Capsule Networks. </span><em>Xinchi Chen, Chunchuan Lyu and Ivan Titov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2993" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3121"><td><span class="poster-title">Learning Programmatic Idioms for Scalable Semantic Parsing. </span><em>Srinivasan Iyer, Alvin Cheung and Luke Zettlemoyer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3121" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3451"><td><span class="poster-title">JuICe: A Large Scale Distantly Supervised Dataset for Open Domain Context-based Code Generation. </span><em>Rajas Agashe, Srinivasan Iyer and Luke Zettlemoyer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3451" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3527"><td><span class="poster-title">Model-based Interactive Semantic Parsing: A Unified Framework and A Text-to-SQL Case Study. </span><em>Ziyu Yao, Yu Su, Huan Sun and Wen-tau Yih</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3527" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3835"><td><span class="poster-title">Modeling Graph Structure in Transformer for Better AMR-to-Text Generation. </span><em>Jie Zhu, Junhui Li, Muhua Zhu, Longhua Qian, Min Zhang and Guodong Zhou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3835" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="72"><td><span class="poster-title">Syntax-Aware Aspect Level Sentiment Classification with Graph Attention Networks. </span><em>Binxuan Huang and Kathleen Carley</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-72" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="281"><td><span class="poster-title">Learning Explicit and Implicit Structures for Targeted Sentiment Analysis. </span><em>Hao Li and Wei Lu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-281" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="317"><td><span class="poster-title">Capsule Network with Interactive Attention for Aspect-Level Sentiment Classification. </span><em>Chunning Du, Haifeng Sun, Jingyu Wang, Qi Qi, Jianxin Liao, Tong Xu and Ming Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-317" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="402"><td><span class="poster-title">Emotion Detection with Neural Personal Discrimination. </span><em>Xiabing Zhou, Zhongqing Wang, Shoushan Li, Guodong Zhou and Min Zhang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-402" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="475"><td><span class="poster-title">Specificity-Driven Cascading Approach for Unsupervised Sentiment Modification. </span><em>Pengcheng Yang, Junyang Lin, Jingjing Xu, Jun Xie, Qi Su and Xu SUN</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-475" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="891"><td><span class="poster-title">LexicalAT: Lexical-Based Adversarial Reinforcement Training for Robust Sentiment Classification. </span><em>Jingjing Xu, Liang Zhao, Hanqi Yan, Qi Zeng, Yun Liang and Xu SUN</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-891" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="896"><td><span class="poster-title">Leveraging Structural and Semantic Correspondence for Attribute-Oriented Aspect Sentiment Discovery. </span><em>Zhe Zhang and Munindar Singh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-896" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="936"><td><span class="poster-title">From the Token to the Review: A Hierarchical Multimodal approach to Opinion Mining. </span><em>Alexandre Garcia, Pierre Colombo, Florence d'Alché-Buc, Slim Essid and Chloé Clavel</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-936" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1477"><td><span class="poster-title">Shallow Domain Adaptive Embeddings for Sentiment Analysis. </span><em>Prathusha K Sarma, Yingyu Liang and William Sethares</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1477" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1691"><td><span class="poster-title">Domain-Invariant Feature Distillation for Cross-Domain Sentiment Classification. </span><em>Mengting Hu, Yike Wu, Shiwan Zhao, Honglei Guo, Renhong Cheng and Zhong Su</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1691" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1705"><td><span class="poster-title">A Novel Aspect-Guided Deep Transition Model for Aspect Based Sentiment Analysis. </span><em>Yunlong Liang, Fandong Meng, Jinchao Zhang, Jinan Xu, Yufeng Chen and Jie Zhou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1705" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1713"><td><span class="poster-title">Human-Like Decision Making: Document-level Aspect Sentiment Classification via Hierarchical Reinforcement Learning. </span><em>Jingjing Wang, Changlong Sun, Shoushan Li, Jiancheng Wang, Luo Si, Min Zhang, Xiaozhong Liu and Guodong Zhou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1713" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1840"><td><span class="poster-title">A Dataset of General-Purpose Rebuttal. </span><em>Matan Orbach, Yonatan Bilu, Ariel Gera, Yoav Kantor, Lena Dankin, Tamar Lavee, Lili Kotlerman, Shachar Mirkin, Michal Jacovi, Ranit Aharonov and Noam Slonim</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1840" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1992"><td><span class="poster-title">Rethinking Attribute Representation and Injection for Sentiment Classification. </span><em>Reinald Kim Amplayo</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1992" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2236"><td><span class="poster-title">A Knowledge Regularized Hierarchical Approach for Emotion Cause Analysis. </span><em>Chuang Fan, Hongyu Yan, Jiachen Du, Lin Gui, Lidong Bing, Min Yang, Ruifeng Xu and Ruibin Mao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2236" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2447"><td><span class="poster-title">Automatic Argument Quality Assessment - New Datasets and Methods. </span><em>Assaf Toledo, Shai Gretz, Edo Cohen-Karlik, Roni Friedman, Elad Venezian, Dan Lahav, Michal Jacovi, Ranit Aharonov and Noam Slonim</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2447" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2493"><td><span class="poster-title">Fine-Grained Analysis of Propaganda in News Article. </span><em>Giovanni Da San Martino, Seunghak Yu, Alberto Barrón-Cedeño, Rostislav Petrov and Preslav Nakov</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2493" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2707"><td><span class="poster-title">Context-aware Interactive Attention for Multi-modal Sentiment and Emotion Analysis. </span><em>Dushyant Singh Chauhan, Md Shad Akhtar, Asif Ekbal and Pushpak Bhattacharyya</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2707" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3182"><td><span class="poster-title">Sequential Learning of Convolutional Features or Effective Text Classification. </span><em>Avinash Madasu and Vijjini Anvesh Rao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3182" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3909"><td><span class="poster-title">The Role of Pragmatic and Discourse Context in Determining Argument Impact. </span><em>Esin Durmus, Faisal Ladhak and Claire Cardie</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3909" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4182"><td><span class="poster-title">Aspect-Level Sentiment Analysis Via Convolution over Dependency Tree. </span><em>Kai Sun, Richong Zhang, Samuel Mensah, Yongyi Mao and Xudong Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4182" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-break-8"><span class="session-title">Coffee Break</span><br/><span class="session-time" title="Thursday, 7 November 2019">15:00 &ndash; 15:30</span></div>
<div class="session-box" id="session-box-11"><div class="session-header" id="session-header-11"> (Session 11)</div>
<div class="session session-expandable session-papers1" id="session-11a"><div id="expander"></div><a href="#" class="session-title">11A: Machine Translation &amp; Multilinguality III</a><br/><span class="session-time" title="Thursday, 7 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-11a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-11a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2192"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Understanding Data Augmentation in Neural Machine Translation: Two Perspectives towards Generalization. </span><em>Guanlin Li, Lemao Liu, Guoping Huang, Conghui Zhu and Tiejun Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2192" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2869"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Simple and Effective Noisy Channel Modeling for Neural Machine Translation. </span><em>Kyra Yee, Yann Dauphin and Michael Auli</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2869" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="745"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">MultiFiT: Efficient Multi-lingual Language Model Fine-tuning. </span><em>Julian Eisenschlos, Sebastian Ruder, Piotr Czapla, Marcin Kadras, Sylvain Gugger and Jeremy Howard</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-745" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1064"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">Hint-Based Training for Non-Autoregressive Machine Translation. </span><em>Zhuohan Li, Zi Lin, Di He, Fei Tian, Tao QIN, Liwei WANG and Tie-Yan Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1064" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-11b"><div id="expander"></div><a href="#" class="session-title">11B: Syntax, Parsing, &amp; Linguistic Theories</a><br/><span class="session-time" title="Thursday, 7 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-11b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-11b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3860"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Working Hard or Hardly Working: Challenges of Integrating Typology into Neural Dependency Parsers. </span><em>Adam Fisch, Jiang Guo and Regina Barzilay</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3860" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1832"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Cross-Lingual BERT Transformation for Zero-Shot Dependency Parsing. </span><em>Yuxuan Wang, Wanxiang Che, Jiang Guo, Yijia Liu and Ting Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1832" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3883"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Multilingual Grammar Induction with Continuous Language Identification. </span><em>Wenjuan Han, Ge Wang, Yong Jiang and Kewei Tu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3883" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2637"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">Quantifying the Semantic Core of Gender Systems. </span><em>Adina Williams, Damian Blasi, Lawrence Wolf-Sonkin, Hanna Wallach and Ryan Cotterell</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2637" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-11c"><div id="expander"></div><a href="#" class="session-title">11C: Sentiment &amp; Social Media</a><br/><span class="session-time" title="Thursday, 7 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-11c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-11c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3447"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Perturbation Sensitivity Analysis to Detect Unintended Model Biases. </span><em>Vinodkumar Prabhakaran, Ben Hutchinson and Margaret Mitchell</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3447" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3519"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Automatically Inferring Gender Associations from Language. </span><em>Serina Chang and Kathy McKeown</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3519" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3715"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">Reporting the Unreported: Event Extraction for Analyzing the Local Representation of Hate Crimes. </span><em>Aida Mostafazadeh Davani, Leigh Yeh, Mohammad Atari, Brendan Kennedy, Gwenyth Portillo Wightman, Elaine Gonzalez, Natalie Delong, Rhea Bhatia, Arineh Mirinjian, Xiang Ren and Morteza Dehghani</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3715" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3493"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">Minimally Supervised Learning of Affective Events Using Discourse Relations. </span><em>Jun Saito, Yugo Murawaki and Sadao Kurohashi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3493" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-11d"><div id="expander"></div><a href="#" class="session-title">11D: Information Extraction IV</a><br/><span class="session-time" title="Thursday, 7 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-11d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-11d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="835"><td id="paper-time">15:30&ndash;15:42</td><td><span class="paper-title">Event Detection with Multi-Order Graph Convolution and Aggregated Attention. </span><em>Haoran Yan, Xiaolong Jin, Xiangbin Meng, Jiafeng Guo and Xueqi Cheng</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-835" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1285"><td id="paper-time">15:42&ndash;15:54</td><td><span class="paper-title">Coverage of Information Extraction from Sentences and Paragraphs. </span><em>Simon Razniewski, Nitisha Jain, Paramita Mirza and Gerhard Weikum</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1285" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2354"><td id="paper-time">15:54&ndash;16:06</td><td><span class="paper-title">HMEAE: Hierarchical Modular Event Argument Extraction. </span><em>Xiaozhi Wang, Ziqi Wang, Xu Han, Zhiyuan Liu, Juanzi Li, Peng Li, Maosong Sun, Jie Zhou and Xiang Ren</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2354" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="3930"><td id="paper-time">16:06&ndash;16:18</td><td><span class="paper-title">Entity, Relation, and Event Extraction with Contextualized Span Representations. </span><em>David Wadden, Ulme Wennberg, Yi Luan and Hannaneh Hajishirzi</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3930" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-11"><div id="expander"></div><a href="#" class="session-title">11 Poster & Demo: Discourse &amp; Pragmatics, Linguistic Theories, Textual Inference, Question Answering, Summarization &amp; Generation </a><br/><span class="session-time" title="Thursday, 7 November 2019">15:30 &ndash; 16:18</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="982"><td><span class="poster-title">Next Sentence Prediction helps Implicit Discourse Relation Classification within and across Domains. </span><em>Wei Shi and Vera Demberg</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-982" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1701"><td><span class="poster-title">Split or Merge: Which is Better for Unsupervised RST Parsing?. </span><em>Naoki Kobayashi, Tsutomu Hirao, Kengo Nakamura, Hidetaka Kamigaito, Manabu Okumura and Masaaki Nagata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1701" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3731"><td><span class="poster-title">BERT for Coreference Resolution: Baselines and Analysis. </span><em>Mandar Joshi, Omer Levy, Luke Zettlemoyer and Daniel Weld</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3731" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3815"><td><span class="poster-title">Linguistic Versus Latent Relations for Modeling Coherent Flow in Paragraphs. </span><em>Dongyeop Kang and Eduard Hovy</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3815" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4125"><td><span class="poster-title">Event Causality Recognition Exploiting Multiple Annotators' Judgments and Background Knowledge. </span><em>Kazuma Kadowaki, Ryu Iida, Kentaro Torisawa, Jong-Hoon Oh and Julien Kloetzer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4125" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1181"><td><span class="poster-title">What Part of the Neural Network Does This? Understanding LSTMs by Measuring and Dissecting Neurons. </span><em>Ji Xin, Jimmy Lin and Yaoliang Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1181" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1227"><td><span class="poster-title">Quantity doesn't buy quality syntax with neural language models. </span><em>Marten van Schijndel, Aaron Mueller and Tal Linzen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1227" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2000"><td><span class="poster-title">Higher-order Comparisons of Sentence Encoder Representations. </span><em>Mostafa Abdou, Artur Kulmizev, Felix Hill, Daniel M. Low and Anders Søgaard</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2000" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2379"><td><span class="poster-title">Text Genre and Training Data Size in Human-like Parsing. </span><em>John Hale, Adhiguna Kuncoro, Keith Hall, Chris Dyer and Jonathan Brennan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2379" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2535"><td><span class="poster-title">Feature2Vec: Distributional semantic modelling of human property knowledge. </span><em>Steven Derby, Paul Miller and Barry Devereux</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2535" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="424"><td><span class="poster-title">Sunny and Dark Outside?! Improving Answer Consistency in VQA through Entailed Question Generation. </span><em>Arijit Ray, Karan Sikka, Ajay Divakaran, Stefan Lee and Giedrius Burachas</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-424" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="961"><td><span class="poster-title">GeoSQA: A Benchmark for Scenario-based Question Answering in the Geography Domain at High School Level. </span><em>Zixian Huang, Yulin Shen, Xiao Li, Yu'ang Wei, Gong Cheng, Lin Zhou, Xinyu Dai and Yuzhong Qu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-961" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1069"><td><span class="poster-title">Revisiting the Evaluation of Theory of Mind through Question Answering. </span><em>Matthew Le, Y-Lan Boureau and Maximilian Nickel</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1069" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1319"><td><span class="poster-title">Multi-passage BERT: A Globally Normalized BERT Model for Open-domain Question Answering. </span><em>Zhiguo Wang, Patrick Ng, Xiaofei Ma, Ramesh Nallapati and Bing Xiang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1319" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2131"><td><span class="poster-title">A Span-Extraction Dataset for Chinese Machine Reading Comprehension. </span><em>Yiming Cui, Ting Liu, Wanxiang Che, Li Xiao, Zhipeng Chen, Wentao Ma, Shijin Wang and Guoping Hu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2131" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2177"><td><span class="poster-title">MICRON: Multigranular Interaction for Contextualizing RepresentatiON in Non-factoid Question Answering. </span><em>Hojae Han, Seungtaek Choi, Haeju Park and Seung-won Hwang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2177" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2229"><td><span class="poster-title">Machine Reading Comprehension Using Structural Knowledge Graph-aware Network. </span><em>Delai Qiu, Yuanzhe Zhang, Xinwei Feng, Xiangwen Liao, Wenbin Jiang, Yajuan Lyu, Kang Liu and Jun Zhao</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2229" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2851"><td><span class="poster-title">Answering Conversational Questions on Structured Data without Logical Forms. </span><em>Thomas Mueller, Francesco Piccinno, Peter Shaw, Massimo Nicosia and Yasemin Altun</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2851" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2859"><td><span class="poster-title">Improving Answer Selection and Answer Triggering using Hard Negatives. </span><em>Sawan Kumar, shweta garg, Kartik Mehta and Nikhil Rasiwasia</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2859" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3163"><td><span class="poster-title">Can You Unpack That? Learning to Rewrite Questions-in-Context. </span><em>Ahmed Elgohary, Denis Peskov and Jordan Boyd-Graber</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3163" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3203"><td><span class="poster-title">Quoref: A Reading Comprehension Dataset with Questions Requiring Coreferential Reasoning. </span><em>Pradeep Dasigi, Nelson F. Liu, Ana Marasovic, Noah A. Smith and Matt Gardner</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3203" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3303"><td><span class="poster-title">Zero-shot Reading Comprehension by Cross-lingual Transfer Learning with Multi-lingual Language Representation Model. </span><em>Tsung-Yuan Hsu, Chi-Liang Liu and Hung-yi Lee</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3303" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3355"><td><span class="poster-title">QuaRTz: An Open-Domain Dataset of Qualitative Relationship Questions. </span><em>Oyvind Tafjord, Matt Gardner, Kevin Lin and Peter Clark</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3355" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3470"><td><span class="poster-title">Giving BERT a Calculator: Finding Operations and Arguments with Reading Comprehension. </span><em>Daniel Andor, Luheng He, Kenton Lee and Emily Pitler</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3470" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4067"><td><span class="poster-title">A Gated Self-attention Memory Network for Answer Selection. </span><em>Tuan Lai, Quan Hung Tran, Trung Bui and Daisuke Kihara</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4067" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="91"><td><span class="poster-title">Polly Want a Cracker: Analyzing Performance of Parroting on Paraphrase Generation Datasets. </span><em>Hong-Ren Mao and Hung-Yi Lee</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-91" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="482"><td><span class="poster-title">Query-focused Sentence Compression in Linear Time. </span><em>Abram Handler and Brendan O'Connor</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-482" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1255"><td><span class="poster-title">Generating Personalized Recipes from Historical User Preferences. </span><em>Bodhisattwa Prasad Majumder, Shuyang Li, Jianmo Ni and Julian McAuley</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1255" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1644"><td><span class="poster-title">Generating Highly Relevant Questions. </span><em>Jiazuo Qiu and Deyi Xiong</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1644" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1674"><td><span class="poster-title">Improving Neural Story Generation by Targeted Common Sense Grounding. </span><em>Huanru Henry Mao, Bodhisattwa Prasad Majumder, Julian McAuley and Garrison Cottrell</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1674" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1963"><td><span class="poster-title">Abstract Text Summarization: A Low Resource Challenge. </span><em>Shantipriya Parida and Petr Motlicek</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1963" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2083"><td><span class="poster-title">Generating Modern Poetry Automatically in Finnish. </span><em>Mika Hämäläinen and Khalid Alnajjar</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2083" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2422"><td><span class="poster-title">SUM-QE: a BERT-based Summary Quality Estimation Model. </span><em>Stratos Xenouleas, Prodromos Malakasiotis, Marianna Apidianaki and Ion Androutsopoulos</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2422" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2870"><td><span class="poster-title">An Empirical Comparison on Imitation Learning and Reinforcement Learning for Paraphrase Generation. </span><em>Wanyu Du and Yangfeng Ji</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2870" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3236"><td><span class="poster-title">Countering the Effects of Lead Bias in News Summarization via Multi-Stage Training and Auxiliary Losses. </span><em>Matt Grenander, Yue Dong, Jackie Chi Kit Cheung and Annie Louis</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3236" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3950"><td><span class="poster-title">Learning Rhyming Constraints using Structured Adversaries. </span><em>Harsh Jhamtani, Sanket Vaibhav Mehta, Jaime Carbonell and Taylor Berg-Kirkpatrick</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3950" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4105"><td><span class="poster-title">Question-type Driven Question Generation. </span><em>Wenjie Zhou, Minghua Zhang and Yunfang Wu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4105" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4107"><td><span class="poster-title">Deep Reinforcement Learning with Distributional Semantic Rewards for Abstractive Summarization. </span><em>Siyao Li, Deren Lei, Pengda Qin and William Yang Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4107" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="285"><td><span class="poster-title">Clause-Wise and Recursive Decoding for Complex and Cross-Domain Text-to-SQL Generation. </span><em>Dongjun Lee</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-285" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1774"><td><span class="poster-title">Do Nuclear Submarines Have Nuclear Captains? A Challenge Dataset for Commonsense Reasoning over Adjectives and Objects. </span><em>James Mullenbach, Jonathan Gordon, Nanyun Peng and Jonathan May</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1774" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2244"><td><span class="poster-title">Aggregating Bidirectional Encoder Representations Using MatchLSTM for Sequence Matching. </span><em>Bo Shao, Yeyun Gong, Weizhen Qi, Nan Duan and Xiaola Lin</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2244" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2765"><td><span class="poster-title">What Does This Word Mean? Explaining Contextualized Embeddings with Natural Language De?nition. </span><em>Ting-Yun Chang and Yun-Nung Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2765" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3058"><td><span class="poster-title">Pre-Training BERT on Domain Resources for Short Answer Grading. </span><em>Chul Sung, Tejas Dhamecha, Swarnadeep Saha, Tengfei Ma, Vinay Reddy and Rishi Arora</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3058" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3276"><td><span class="poster-title">WIQA: A dataset for `What if...` reasoning over procedural text. </span><em>Niket Tandon, Bhavana Dalvi, Keisuke Sakaguchi, Peter Clark and Antoine Bosselut</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3276" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3606"><td><span class="poster-title">Evaluating BERT for natural language inference: A case study on the CommitmentBank. </span><em>Nanjiang Jiang and Marie-Catherine de Marneffe</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3606" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3974"><td><span class="poster-title">Incorporating Domain Knowledge into Medical NLI using Knowledge Graphs. </span><em>Soumya Sharma, Bishal Santra, Abhik Jana, Santosh Tokala, Niloy Ganguly and Pawan Goyal</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3974" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-break-9"><span class="session-title">Mini-Break</span><br/><span class="session-time" title="Thursday, 7 November 2019">16:18 &ndash; 16:30</span></div>
<div class="session-box" id="session-box-12"><div class="session-header" id="session-header-12"> (Session 12)</div>
<div class="session session-expandable session-papers1" id="session-12a"><div id="expander"></div><a href="#" class="session-title">12A: Machine Translation &amp; Multilinguality IV</a><br/><span class="session-time" title="Thursday, 7 November 2019">16:30 &ndash; 17:24</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-12a-selector"> Choose All</a><a href="#" class="session-deselector" id="session-12a-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="3349"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">The FLORES Evaluation Datasets for Low-Resource Machine Translation: NepaliñEnglish and SinhalañEnglish. </span><em>Francisco Guzmán, Peng-Jen Chen, Myle Ott, Juan Pino, Guillaume Lample, Philipp Koehn, Vishrav Chaudhary and Marc'Aurelio Ranzato</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3349" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1204"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Mask-Predict: Parallel Decoding of Conditional Masked Language Models. </span><em>Marjan Ghazvininejad, Omer Levy, Yinhan Liu and Luke Zettlemoyer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1204" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="777"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Learning to Copy for Automatic Post-Editing. </span><em>Xuancheng Huang, Yang Liu, Huanbo Luan, Jingfang Xu and Maosong Sun</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-777" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers2" id="session-12b"><div id="expander"></div><a href="#" class="session-title">12B: Lexical Semantics III</a><br/><span class="session-time" title="Thursday, 7 November 2019">16:30 &ndash; 17:24</span><br/><span class="session-location btn btn--info btn--location">201A + 201B</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-12b-selector"> Choose All</a><a href="#" class="session-deselector" id="session-12b-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="1912"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Exploring Human Gender Stereotypes with Word Association Test. </span><em>Yupei Du, Yuanbin Wu and Man Lan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1912" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="TACL-1729"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Still a Pain in the Neck: Evaluating Text Representations on Lexical Composition. </span><em>Vered Shwartz and Ido Dagan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1729" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="TACL-1648"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Where's My Head? Definition, Dataset and Models for Numeric Fused-Heads Identification and Resolution. </span><em>Yanai Elazar and Yoav Goldberg</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1648" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers3" id="session-12c"><div id="expander"></div><a href="#" class="session-title">12C: Generation III</a><br/><span class="session-time" title="Thursday, 7 November 2019">16:30 &ndash; 17:24</span><br/><span class="session-location btn btn--info btn--location">203+204+205</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-12c-selector"> Choose All</a><a href="#" class="session-deselector" id="session-12c-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="2725"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">A Modular Architecture for Unsupervised Sarcasm Generation. </span><em>Abhijit Mishra, Tarun Tater and Karthik Sankaranarayanan</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2725" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="2534"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Generating Classical Chinese Poems from Vernacular Chinese. </span><em>Zhichao Yang, Pengshan Cai, Yansong Feng, Fei Li, Weijiang Feng, Elena Suet-Ying Chiu and hong yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2534" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="724"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">Set to Ordered Text: Generating Discharge Instructions from Medical Billing Codes. </span><em>Litton J Kurisinkel and Nancy Chen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-724" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-papers4" id="session-12d"><div id="expander"></div><a href="#" class="session-title">12D: Phonology, Word Segmentation, &amp; Parsing</a><br/><span class="session-time" title="Thursday, 7 November 2019">16:30 &ndash; 17:24</span><br/><span class="session-location btn btn--info btn--location">201C</span><br/><div class="paper-session-details"><br/><a href="#" class="session-selector" id="session-12d-selector"> Choose All</a><a href="#" class="session-deselector" id="session-12d-deselector">Remove All</a><table class="paper-table"><tr><td class="session-chair" colspan="2">Chair: <a href="mailto:TBD-email">TBD</a></td></tr>
<tr id="paper" paper-id="451"><td id="paper-time">16:30&ndash;16:48</td><td><span class="paper-title">Constraint-based Learning of Phonological Processes. </span><em>Shraddha Barke, Rose Kunkel, Nadia Polikarpova, Eric Meinhardt, Eric Bakovic and Leon Bergen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-451" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="1340"><td id="paper-time">16:48&ndash;17:06</td><td><span class="paper-title">Detect Camouflaged Spam Content via StoneSkipping: Graph and Text Joint Embedding for Chinese Character Variation Representation. </span><em>Zhuoren Jiang, Zhe Gao, Guoxiu He, Yangyang Kang, Changlong Sun, Qiong Zhang, Luo Si and Xiaozhong Liu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1340" aria-hidden="true"></i></td></tr>
<tr id="paper" paper-id="TACL-1582"><td id="paper-time">17:06&ndash;17:24</td><td><span class="paper-title">A Generative Model for Punctuation in Dependency Trees. </span><em>Xiang Lisa Li, Dingquan Wang and Jason Eisner</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-TACL-1582" aria-hidden="true"></i></td></tr>
</table></div></div>
<div class="session session-expandable session-posters" id="session-poster-12"><div id="expander"></div><a href="#" class="session-title">12 Poster & Demo: Information Extraction, Text Mining &amp; NLP Applications, Social Media &amp; Computational Social Science, Sentiment Analysis &amp; Argument Mining </a><br/><span class="session-time" title="Thursday, 7 November 2019">16:30 &ndash; 17:24</span><br/><span class="session-location btn btn--info btn--location">Hall 2A</span><div class="poster-session-details"><br/><table class="poster-table">
<tr id="poster" poster-id="189"><td><span class="poster-title">An Attentive Fine-Grained Entity Typing Model with Latent Type Representation. </span><em>Ying Lin and Heng Ji</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-189" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="193"><td><span class="poster-title">An Improved Neural Baseline for Temporal Relation Extraction. </span><em>Qiang Ning, Sanjay Subramanian and Dan Roth</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-193" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="822"><td><span class="poster-title">Improving Fine-grained Entity Typing with Entity Linking. </span><em>Hongliang Dai, Donghong Du, Xin Li and Yangqiu Song</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-822" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1222"><td><span class="poster-title">Combining Spans into Entities: A Neural Two-Stage Approach for Recognizing Discontiguous Entities. </span><em>Bailin Wang and Wei Lu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1222" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1686"><td><span class="poster-title">Cross-Sentence N-ary Relation Extraction using Lower-Arity Universal Schemas. </span><em>Kosuke Akimoto, Takuya Hiraoka, Kunihiko Sadamasa and Mathias Niepert</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1686" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1760"><td><span class="poster-title">Gazetteer-Enhanced Attentive Neural Networks for Named Entity Recognition. </span><em>Hongyu Lin, Yaojie Lu, Xianpei Han, Le Sun, Bin Dong and Shanshan Jiang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1760" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1782"><td><span class="poster-title">`A Buster Keaton of Linguistics`: First Automated Approaches for the Extraction of Vossian Antonomasia. </span><em>Michel Schwab, Robert Jäschke, Frank Fischer and Jannik Strötgen</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1782" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1799"><td><span class="poster-title">Multi-Task Learning for Chemical Named Entity Recognition with Chemical Compound Paraphrasing. </span><em>Taiki Watanabe, Akihiro Tamura, Takashi Ninomiya, Takuya Makino and Tomoya Iwakura</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1799" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2697"><td><span class="poster-title">FewRel 2.0: Towards More Challenging Few-Shot Relation Classification. </span><em>Tianyu Gao, Xu Han, Hao Zhu, Zhiyuan Liu, Peng Li, Maosong Sun and Jie Zhou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2697" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2992"><td><span class="poster-title">ner and pos when nothing is capitalized. </span><em>Stephen Mayhew, Tatiana Tsygankova and Dan Roth</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2992" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4099"><td><span class="poster-title">CaRB: A Crowdsourced Benchmark for Open IE. </span><em>Sangnie Bhardwaj, Samarth Aggarwal and Mausam -</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4099" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4158"><td><span class="poster-title">Weakly Supervised Attention Networks for Entity Recognition. </span><em>Barun Patra and Joel Ruben Antony Moniz</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4158" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="19"><td><span class="poster-title">Revealing and Predicting Online Persuasion Strategy with Elementary Units. </span><em>Gaku Morio, Ryo Egawa and Katsuhide Fujita</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-19" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="849"><td><span class="poster-title">A Challenge Dataset and Effective Models for Aspect-Based Sentiment Analysis. </span><em>Qingnan Jiang, Lei Chen, Ruifeng Xu, Xiang Ao and Min Yang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-849" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1157"><td><span class="poster-title">Learning with Noisy Labels for Sentence-level Sentiment Classification. </span><em>Hao Wang, Bing Liu, Chaozhuo Li, Yan Yang and Tianrui Li</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1157" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1347"><td><span class="poster-title">DENS: A Dataset for Multi-class Emotion Analysis. </span><em>Chen Liu, Muhammad Osama and Anderson De Andrade</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1347" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3016"><td><span class="poster-title">Multi-Task Stance Detection with Sentiment and Stance Lexicons. </span><em>Yingjie Li and Cornelia Caragea</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3016" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3085"><td><span class="poster-title">A Robust Self-Learning Framework for Cross-Lingual Text Classification. </span><em>Xin Dong and Gerard de Melo</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3085" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3869"><td><span class="poster-title">Learning to Flip the Sentiment of Reviews from Non-Parallel Corpora. </span><em>Canasai Kruengkrai</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3869" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="80"><td><span class="poster-title">Label Embedding using Hierarchical Structure of Labels for Twitter Classification. </span><em>Taro Miyazaki, Kiminobu Makino, Yuka Takei, Hiroki Okamoto and Jun Goto</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-80" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="393"><td><span class="poster-title">Interpretable Word Embeddings via Informative Priors. </span><em>Miriam Hurtado Bodell, Martin Arvidsson and Måns Magnusson</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-393" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2101"><td><span class="poster-title">Adversarial Removal of Demographic Attributes Revisited. </span><em>Maria Barrett, Yova Kementchedjhieva, Yanai Elazar, Desmond Elliott and Anders Søgaard</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2101" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2170"><td><span class="poster-title">A deep-learning framework to detect sarcasm targets. </span><em>Jasabanta Patro, Srijan Bansal and Animesh Mukherjee</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2170" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2759"><td><span class="poster-title">In Plain Sight: Media Bias Through the Lens of Factual Reporting. </span><em>Lisa Fan, Marshall White, Eva Sharma, Ruisi Su, Prafulla Kumar Choubey, Ruihong Huang and Lu Wang</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2759" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3333"><td><span class="poster-title">Incorporating Label Dependencies in Multilabel Stance Detection. </span><em>William Ferreira and Andreas Vlachos</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3333" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3345"><td><span class="poster-title">Investigating Sports Commentator Bias within a Large Corpus of American Football Broadcasts. </span><em>Jack Merullo, Luke Yeh, Abram Handler, Alvin Grissom II, Brendan O'Connor and Mohit Iyyer</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3345" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="759"><td><span class="poster-title">Charge-Based Prison Term Prediction with Deep Gating Network. </span><em>Huajie Chen, Deng Cai, Wei Dai, Zehui Dai and Yadong Ding</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-759" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1020"><td><span class="poster-title">Restoring ancient text using deep learning: a case study on Greek epigraphy. </span><em>Yannis Assael, Thea Sommerschield and Jonathan Prag</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1020" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1068"><td><span class="poster-title">Embedding Lexical Features via Tensor Decomposition for Small Sample Humor Recognition. </span><em>Zhenjie Zhao, Andrew Cattle, Evangelos Papalexakis and Xiaojuan Ma</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1068" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1192"><td><span class="poster-title">EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks. </span><em>Jason Wei and Kai Zou</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1192" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1581"><td><span class="poster-title">Neural News Recommendation with Multi-Head Self-Attention. </span><em>Chuhan Wu, Fangzhao Wu, Suyu Ge, Tao Qi, Yongfeng Huang and Xing Xie</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1581" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1611"><td><span class="poster-title">What Matters for Neural Cross-Lingual Named Entity Recognition: An Empirical Analysis. </span><em>Xiaolei Huang, Jonathan May and Nanyun Peng</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1611" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1737"><td><span class="poster-title">Telling the Whole Story: A Manually Annotated Chinese Dataset for the Analysis of Humor in Jokes. </span><em>Dongyu Zhang, Heting Zhang, Xikai Liu, Hongfei LIN and Feng Xia</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1737" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="1763"><td><span class="poster-title">Generating Natural Anagrams: Towards Language Generation Under Hard Combinatorial Constraints. </span><em>Masaaki Nishino, Sho Takase, Tsutomu Hirao and Masaaki Nagata</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-1763" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2013"><td><span class="poster-title">STANCY: Stance Classification Based on Consistency Cues. </span><em>Kashyap Popat, Subhabrata Mukherjee, Andrew Yates and Gerhard Weikum</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2013" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2551"><td><span class="poster-title">Cross-lingual intent classification in a low resource industrial setting. </span><em>Talaat Khalil, Kornel Kielczewski, Georgios Christos Chouliaras, Amina Keldibek and Maarten Versteegh</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2551" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2839"><td><span class="poster-title">SoftRegex: Generating Regex from Natural Language Descriptions using Softened Regex Equivalence. </span><em>Jun-U Park, Sang-Ki Ko, Marco Cognetta and Yo-Sub Han</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2839" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="2907"><td><span class="poster-title">Using Clinical Notes with Time Series Data for ICU Management. </span><em>Swaraj Khadanga, Karan Aggarwal, Shafiq Joty and Jaideep Srivastava</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-2907" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3639"><td><span class="poster-title">Spelling-Aware Construction of Macaronic Texts for Teaching Foreign-Language Vocabulary. </span><em>Adithya Renduchintala, Philipp Koehn and Jason Eisner</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3639" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="3718"><td><span class="poster-title">Towards Machine Reading for Interventions from Humanitarian-Assistance Program Literature. </span><em>Bonan Min, Yee Seng Chan, Haoling Qiu and Joshua Fasching</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-3718" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="4014"><td><span class="poster-title">RUN through the Streets: A New Dataset and Baseline Models for Realistic Urban Navigation. </span><em>Tzuf Paz-Argaman and Reut Tsarfaty</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-4014" aria-hidden="true"></i></td></tr>
<tr id="poster" poster-id="162"><td><span class="poster-title">Context-Aware Conversation Thread Detection in Multi-Party Chat. </span><em>Ming Tan, Dakuo Wang, Yupeng Gao, Haoyu Wang, Saloni Potdar, Xiaoxiao Guo, Shiyu Chang and Mo Yu</em>&nbsp;&nbsp;<i class="fa fa-file-pdf-o paper-icon" data="http://aclweb.org/anthology/TBD-162" aria-hidden="true"></i></td></tr>
</table></div></div>
</div>
<div class="session session-break session-plenary" id="session-break-10"><span class="session-title">Mini-Break</span><br/><span class="session-time" title="Thursday, 7 November 2019">17:24 &ndash; 17:30</span></div>
<div class="session session-expandable session-papers-best"><div id="expander"></div><a href="#" class="session-title">Best Paper Awards and Closing</a><br/><span class="session-time" title="Thursday, 7 November 2019">17:30 &ndash; 18:00</span><br/><span class="session-location btn btn--info btn--location">Hall 2C</span><br/><div class="paper-session-details"><br/><table class="paper-table">
</table></div></div>




<!-- PDF PRINTING BUTTON -->

</div>
<div id="generatePDFForm">
	<div id="formContainer">
		<input type="checkbox" id="includePlenaryCheckBox" value="second_checkbox"/>&nbsp;&nbsp;<span id="checkBoxLabel">Include plenary sessions in schedule</span>
        <br/>
         <a href="#" id="generatePDFButton" class="btn btn--info btn--large">Download PDF</a>
	</div>
</div>