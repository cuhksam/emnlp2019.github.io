---
title: Main Conference Program
layout: schedule
excerpt: "EMNLP 2018 conference program."
permalink: /program-beta
sidebar: false
script: |
    <script type="text/javascript">

        sessionInfoHash = {};
        paperInfoHash = {};
        chosenPapersHash = {};
        chosenTutorialsHash = {};
        chosenPostersHash = {};
        plenarySessionHash = {};
        includePlenaryInSchedule = true;
        helpShown = false;

        var instructions = "<div id=\"popupInstructionsDiv\"><div id=\"title\">Help</div><div id=\"popupInstructions\"><ul><li>Click on a the \"<strong>+</strong>\" button or the title of a session to toggle it. </li> <li>Click on a tutorial/paper/poster to toggle its selection. </li> <li>You can select more than one paper for a time slot. </li> <li>Click the <strong>\"Download PDF\"</strong> button at the bottom to download your customized PDF. </li> <li>To expand a parallel sessions simultaneously, hold Shift and click on any of them. </li> <li>On non-mobile devices, hovering on a paper for a time slot highlights it in yellow and its conflicting papers in red. Hovering on papers already selected for a time slot (or their conflicts) highlights them in green. </li> <li>The PDF might have some blank rows at the bottom as padding to avoid rows being split across pages.</li> <li>While saving the generated PDF on mobile devices, its name cannot be changed.</li> </ul></div></div>";

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
                    doc.text('(Generated via http://emnlp2018.org/program)', data.settings.margin.left, doc.internal.pageSize.height - 10);
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

        function makePosterRows(titles, types, sessions) {
            var numPosters = titles.length;
            var sessionStart = sessions[0].start;
            var sessionEnd = sessions[0].end;
            rows = ['<tr><td rowspan=' + (numPosters + 1) + ' class="time">' + sessionStart + '&ndash;' + sessionEnd + '</td><td rowspan=' + (numPosters + 1) + ' class="location">' + sessions[0].location + '</td><td class="info-paper">' + sessions[0].title +  '</td></tr>'];
            for (var i=0; i<numPosters; i++) {
                var title = titles[i];
                var type = types[i];
                rows.push('<tr><td></td><td></td><td class="info-poster">' + title + ' [' + type + ']</td></tr>');
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

            /* since papers and posters might start at the same time we cannot just rely on starting times to differentiate papers vs. posters. so, what we can do is just add an item type before we do the concatenation and then rely on that item type to distinguish the item */
            
            var nonPlenaryKeysAndTypes = [];
            var tutorialKeys = Object.keys(chosenTutorialsHash);
            var posterKeys = Object.keys(chosenPostersHash);
            var paperKeys = Object.keys(chosenPapersHash);
            for (var i=0; i < tutorialKeys.length; i++) {
                nonPlenaryKeysAndTypes.push([tutorialKeys[i], 'tutorial']);
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

            $('span.session-location, span.inline-location').on('click', function(event) {
                event.stopPropagation();
            });

            $('span.session-external-location').on('click', function(event) {
                var placeName = $(this).text().trim().replace(" ", "+");
                window.open("https://www.google.com/maps/place/" + placeName, "_blank");
                event.stopPropagation();
            });

            /* show the floorplan when any location is clicked */
            $('span.session-location, span.inline-location').magnificPopup({
                items: {
                    src: '/images/westin-floor-plan.png'
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
                return this.id.match(/session-\d[a-z]$/);
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
                var paperTitle = paperTimeObj.siblings('td').text().trim();

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
                var exactSessionStartingTime = session.day + sessionStart;
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
                var numChosenItems = Object.keys(chosenPapersHash).length + Object.keys(chosenTutorialsHash).length + Object.keys(chosenPostersHash).length;
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

<div class="schedule">
    <div class="day" id="first-day">Wednesday, October 31, 2018</div>
    <div class="session session-expandable session-tutorials" id="session-morning-tutorials1">
        <div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/>
        <span class="session-time">9:00 &ndash; 12:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T1] Joint Models for NLP.</strong> Yue Zhang.</span> <br/><span class="btn btn--info btn--location inline-location">Mackenzie</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T2] Graph Formalisms for Meaning Representations.</strong> Adam Lopez and Sorcha Gilroy.</span><br/><span href="#" class="btn btn--info btn--location inline-location">Salon 1</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-1">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 &ndash; 14:00</span>
    </div>    
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials1">
        <div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/>
        <span class="session-time">14:00 &ndash; 17:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T3] Writing Code for NLP Research.</strong> Matt Gardner, Mark Neumann, Joel Grus, and Nicholas Lourie. </span><br/><span href="#" class="btn btn--info btn--location inline-location">Salons A/B</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-with-location session-plenary" id="session-reception">
        <div id="expander"></div><a href="#" class="session-title">Welcome Reception</a><br/>        
        <span class="session-time">18:00 &ndash; 21:00</span><br/>
        <span class="session-location btn btn--info btn--location">Bayshore Grand Ballroom</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>Catch up with your colleagues at the Welcome Reception!  It will be held immediately following the tutorials at the Westin Bayshore Hotel, Sunday, July 30th, in the Bayshore Grand Ballroom (the conference venue).  Refreshments and a light dinner will be provided and a cash bar will be available.</p>
            </div>
        </div>
    </div>
    <div class="day" id="second-day">Thursday, November 1, 2018</div>
    <div class="session session-expandable session-tutorials" id="session-morning-tutorials2">
        <div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/>
        <span class="session-time">09:00 &ndash; 12:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T4] Deep Latent Variable Models of Natural Language.</strong> Alexander Rush, Yoon Kim, and Sam Wiseman.</span> <br/><span class="btn btn--info btn--location inline-location">Mackenzie</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T5] Standardized Tests as benchmarks for Artificial Intelligence.</strong> Mrinmaya Sachan, Minjoon Seo, Hannaneh Hajishirzi, and Eric Xing.</span><br/><span href="#" class="btn btn--info btn--location inline-location">Salon 1</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-2">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 &ndash; 14:00</span>
    </div>    
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials2">
        <div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/>
        <span class="session-time">14:00 &ndash; 17:30</span><br/>
        <div class="tutorial-session-details">
            <br/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title"><strong>[T4] Deep Chit-Chat: Deep Learning for ChatBots.</strong> Wei Wu and Rui Yan. </span><br/><span href="#" class="btn btn--info btn--location inline-location">Salons A/B</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="day" id="third-day">Friday, November 2</div>
    <div class="session session-plenary" id="session-welcome">
        <span class="session-title">Opening Remarks</span><br/>
        <span class="session-time">9:00 AM &ndash; 9:30 AM</span><br/>
        <span class="session-location btn btn--info btn--location">Gold Hall</span>
    </div>
    <div class="session session-expandable session-plenary" id="session-invited-julia">
        <div id="expander"></div><a href="#" class="session-title">Invited Talk: Truth or Lie? Spoken Indicators of Deception in Speech</a><br/>        
        <span class="session-people">Julia Hirschberg (Columbia University)</span><br/>
        <span class="session-time">9:30 AM &ndash; 10:30 AM</span><br/>
        <span class="session-location btn btn--info btn--location">Gold Hall</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>Detecting deception from various forms of human behavior is a longstanding research goal which is of considerable interest to the military, law enforcement, corporate security, social services and mental health workers. However, both humans and polygraphs are very poor at this task. We describe more accurate methods we have developed to detect deception automatically from spoken language. Our classifiers are trained on the largest cleanly recorded corpus of within-subject deceptive and non-deceptive speech that has been collected. To distinguish truth from lie we make use of acoustic-prosodic, lexical, demographic, and personality features. We further examine differences in deceptive behavior based upon gender, personality, and native language (Mandarin Chinese vs. English), comparing our systems to human performance. We extend our studies to identify cues in trusted speech vs. mistrusted speech and how these features differ by speaker and by listener. Why does a listener believe a lie?</p>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-1">
        <span class="session-title">Coffee Break</span><br/>        
        <span class="session-time">10:30 AM &ndash; 11:00 AM</span>
    </div>
    <div class="session-box" id="session-box-1">
        <div class="session-header" id="session-header-1">Long Papers and Demos (Orals &amp; Posters) I</div>
        <div class="session session-expandable session-papers1" id="session-1a">
            <div id="expander"></div><a href="#" class="session-title">1A: Information Extraction</a><br/>
                <span class="session-time">11:00 &ndash; 12:30</span>
                <br/>
                <span class="session-location btn btn--info btn--location">Gold Hall</span>
                <br/>
                <div class="paper-session-details">
                    <br/>
                    <a href="#" class="session-selector" id="session-1a-selector">
                    Choose All</a>
                    <a href="#" class="session-deselector" id="session-1a-deselector">Remove All</a>
                    <table class="paper-table">
                        <tr>
                            <td class="session-chair" colspan="2">Chair: Zornitsa Kozareva</td>
                        </tr>
                        <tr id="paper" paper-id="1">
                            <td id="paper-time">11:00&ndash;11:18</td>
                            <td>
                                <span class="paper-title">Adversarial Multi-task Learning for Text Classification. </span><em>Pengfei Liu, Xipeng Qiu and Xuanjing Huang</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="2">
                            <td id="paper-time">11:18&ndash;11:36</td>
                            <td>
                                <span class="paper-title">Neural End-to-End Learning for Computational Argumentation Mining. </span><em>Steffen Eger, Johannes Daxenberger and Iryna Gurevych</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="3">
                            <td id="paper-time">11:36&ndash;11:54</td>
                            <td>
                                <span class="paper-title">Neural Symbolic Machines: Learning Semantic Parsers on Freebase with Weak Supervision. </span><em>Chen Liang, Jonathan Berant, Quoc Le, Kenneth D. Forbus and Ni Lao</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="4">
                            <td id="paper-time">11:54&ndash;12:12</td>
                            <td>
                                <span class="paper-title">Neural Relation Extraction with Multi-lingual Attention. </span><em>Yankai Lin, Zhiyuan Liu and Maosong Sun</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="5">
                            <td id="paper-time">12:12&ndash;12:30</td>
                            <td>
                                <span class="paper-title">Classifying Temporal Relations by Bidirectional LSTM over Dependency Paths. </span><em>Fei Cheng and Yusuke Miyao</em>
                            </td>
                        </tr>
                    </table>
                </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-1b">
            <div id="expander"></div><a href="#" class="session-title">1B: Semantics</a><br/>
                <span class="session-time">11:00 &ndash; 12:30</span>
                <br/>
                <span class="session-location btn btn--info btn--location">Copper Hall</span>
                <br/>
                <div class="paper-session-details">
                    <br/>
                    <a href="#" class="session-selector" id="session-1b-selector">
                    Choose All</a>
                    <a href="#" class="session-deselector" id="session-1b-deselector">Remove All</a>
                    <table class="paper-table">
                        <tr>
                            <td class="session-chair" colspan="2">Chair: Preslav Nakov</td>
                        </tr>
                        <tr id="paper" paper-id="6">
                            <td id="paper-time">11:00&ndash;11:18</td>
                            <td>
                                <span class="paper-title">Learning Structured Natural Language Representations for Semantic Parsing. </span><em>Jianpeng Cheng, Siva Reddy, Vijay Saraswat and Mirella Lapata</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="7">
                            <td id="paper-time">11:18&ndash;11:36</td>
                            <td>
                                <span class="paper-title">Morph-fitting: Fine-Tuning Word Vector Spaces with Simple Language-Specific Rules. </span><em>Ivan Vulić, Nikola Mrkšić, Roi Reichart, Diarmuid Ó Séaghdha, Steve Young and Anna Korhonen</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="8">
                            <td id="paper-time">11:36&ndash;11:54</td>
                            <td>
                                <span class="paper-title">Skip-Gram – Zipf + Uniform = Vector Additivity. </span><em>Alex Gittens, Dimitris Achlioptas and Michael W. Mahoney</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="9">
                            <td id="paper-time">11:54&ndash;12:12</td>
                            <td>
                                <span class="paper-title">The State of the Art in Semantic Representation. </span><em>Omri Abend and Ari Rappoport</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="10">
                            <td id="paper-time">12:12&ndash;12:30</td>
                            <td>
                                <span class="paper-title">AMR-to-text Generation with Synchronous Node Replacement Grammar. </span><em>Linfeng Song, Xiaochang Peng, Yue Zhang, Zhiguo Wang and Daniel Gildea</em>
                            </td>
                        </tr>
                    </table>
                </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-1c">
            <div id="expander"></div><a href="#" class="session-title">1C: Discourse</a><br/>
                <span class="session-time">11:00 &ndash; 12:30</span>
                <br/>
                <span class="session-location btn btn--info btn--location">Silver Hall</span>
                <br/>
                <div class="paper-session-details">
                    <br/>
                    <a href="#" class="session-selector" id="session-1c-selector">
                    Choose All</a>
                    <a href="#" class="session-deselector" id="session-1c-deselector">Remove All</a>
                    <table class="paper-table">
                        <tr>
                            <td class="session-chair" colspan="2">Chair: Yangfeng Ji</td>
                        </tr>
                        <tr id="paper" paper-id="11">
                            <td id="paper-time">11:00&ndash;11:18</td>
                            <td>
                                <span class="paper-title">Joint Learning for Coreference Resolution. </span><em>Jing Lu and Vincent Ng</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="12">
                            <td id="paper-time">11:18&ndash;11:36</td>
                            <td>
                                <span class="paper-title">Generating and Exploiting Large-scale Pseudo Training Data for Zero Pronoun Resolution. </span><em>Ting Liu, Yiming Cui, Qingyu Yin, Wei-Nan Zhang, Shijin Wang and Guoping Hu</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="13">
                            <td id="paper-time">11:36&ndash;11:54</td>
                            <td>
                                <span class="paper-title">Discourse Mode Identification in Essays. </span><em>Wei Song, Dong Wang, Ruiji Fu, Lizhen Liu, Ting Liu and Guoping Hu</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="14">
                            <td id="paper-time">11:54&ndash;12:12</td>
                            <td>
                                <span class="paper-title">[TACL] Winning on the Merits: The Joint Effects of Content and Style on Debate Outcomes. </span><em>Lu Wang, Nick Beauchamp, Sarah Shugars, Kechen Qin</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="15">
                            <td id="paper-time">12:12&ndash;12:30</td>
                            <td>
                                <span class="paper-title">Lexical Features in Coreference Resolution: To be Used With Caution. </span><em>Nafise Sadat Moosavi and Michael Strube</em>
                            </td>
                        </tr>
                    </table>
                </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-1d">
            <div id="expander"></div><a href="#" class="session-title">1D: Machine Translation</a><br/>
                <span class="session-time">11:00 &ndash; 12:30</span>
                <br/>
                <span class="session-location btn btn--info btn--location">Hall 100</span>
                <br/>
                <div class="paper-session-details">
                    <br/>
                    <a href="#" class="session-selector" id="session-1d-selector">
                    Choose All</a>
                    <a href="#" class="session-deselector" id="session-1d-deselector">Remove All</a>
                    <table class="paper-table">
                        <tr>
                            <td class="session-chair" colspan="2">Chair: Haitao Mi</td>
                        </tr>
                        <tr id="paper" paper-id="16">
                            <td id="paper-time">11:00&ndash;11:18</td>
                            <td>
                                <span class="paper-title">A Convolutional Encoder Model for Neural Machine Translation. </span><em>Jonas Gehring, Michael Auli, David Grangier and Yann Dauphin</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="17">
                            <td id="paper-time">11:18&ndash;11:36</td>
                            <td>
                                <span class="paper-title">Deep Neural Machine Translation with Linear Associative Unit. </span><em>Mingxuan Wang, Zhengdong Lu, Jie Zhou and Qun Liu</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="18">
                            <td id="paper-time">11:36&ndash;11:54</td>
                            <td>
                                <span class="paper-title">[TACL] A Polynomial-Time Dynamic Programming Algorithm for Phrase-Based Decoding with a Fixed Distortion Limit. </span><em>Yin-Wen Chang and Michael Collins</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="19">
                            <td id="paper-time">11:54&ndash;12:12</td>
                            <td>
                                <span class="paper-title">[TACL] Context Gates for Neural Machine Translation. </span><em>Zhaopeng Tu, Yang Liu, Zhengdong Lu, Xiaohua Liu and Hang Li</em>
                            </td>
                        </tr>
                        <tr id="paper" paper-id="20">
                            <td id="paper-time">12:12&ndash;12:30</td>
                            <td>
                                <span class="paper-title">Alternative Objective Functions for Training MT Evaluation Metrics. </span><em>Miloš Stanojević and Khalil Sima’an</em>
                            </td>
                        </tr>
                    </table>
                </div>
        </div>
       <div class="session session-expandable session-posters" id="session-poster-1">
            <div id="expander"></div><a href="#" class="session-title">1E: Posters &amp; Demos</a><br/>        
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <h4 class="poster-type">Topic 1</h4>
                <table class="poster-table">
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Enriching Complex Networks with Word Embeddings for Detecting Mild Cognitive Impairment from Speech Transcripts. </span><em>Leandro Santos, Edilson Anselmo Corrêa Júnior, Osvaldo Oliveira Jr, Diego Amancio, Letícia Mansur and Sandra Aluísio</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Adversarial Adaptation of Synthetic or Stale Data. </span><em>Young-Bum Kim, Karl Stratos and Dongchan Kim</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Chat Detection in Intelligent Assistant: Combining Task-oriented and Non-task-oriented Spoken Dialogue Systems. </span><em>Satoshi Akasaki and Nobuhiro Kaji</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">A Neural Local Coherence Model. </span><em>Dat Tien Nguyen and Shafiq Joty</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Data-Driven Broad-Coverage Grammars for Opinionated Natural Language Generation (ONLG). </span><em>Tomer Cagan, Stefan L. Frank and Reut Tsarfaty</em>
                        </td>
                    </tr>
                </table>
                <h4 class="poster-type">Topic 2</h4>
                <table class="poster-table">
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Neural Architecture for Temporal Relation Extraction: A Bi-LSTM Approach for Detecting Narrative Containers. </span><em>Julien Tourille, Olivier Ferret, Aurelie Neveol and Xavier Tannier</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">How to Make Contexts More Useful? An Empirical Study on Context-Aware Neural Conversation Models. </span><em>Zhiliang Tian, Rui Yan, Lili Mou, Yiping Song, Yansong Feng and Dongyan Zhao</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Cross-lingual and cross-domain discourse segmentation of entire documents. </span><em>Chloé Braud, Ophélie Lacroix and Anders Søgaard</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Detecting Good Arguments in a Non-Topic-Specific Way: An Oxymoron?. </span><em>Beata Beigman Klebanov, Binod Gyawali and Yi Song</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Argumentation Quality Assessment: Theory vs. Practice. </span><em>Henning Wachsmuth, Nona Naderi, Ivan Habernal, Yufang Hou, Graeme Hirst, Iryna Gurevych and Benno Stein</em>
                        </td>
                    </tr>
                </table>
                <h4 class="poster-type">Topic 3</h4>
                <table class="poster-table">
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Computational Characterization of Mental States: A Natural Language Processing Approach. </span><em>Facundo Carrillo</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Improving Distributed Representations of Tweets - Present and Future. </span><em>Ganesh Jawahar</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">Bilingual Word Embeddings with Bucketed CNN for Parallel Sentence Extraction. </span><em>Jeenu Grover and Pabitra Mitra</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">nQuery - A Natural Language Statement to SQL Query Generator. </span><em>Nandan Sukthankar, Sanket Maharnawar, Pranay Deshmukh, Yashodhara Haribhakta and Vibhavari Kamble</em>
                        </td>
                    </tr>
                    <tr id="poster">
                        <td>
                            <span class="poster-title">V for Vocab : An Intelligent Flashcard Application. </span><em>Nihal V. Nayak, Tanmay Chinchore, Aishwarya Hanumanth Rao, Shane Michael Martin, Sagar Nagaraj Simha, G. M. Lingaraju and H. S. Jamadagni</em>
                        </td>
                    </tr>                
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-3">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 &ndash; 13:45</span>
    </div> 
    <div id="generatePDFForm">
        <div id="formContainer">
            <input type="checkbox" id="includePlenaryCheckBox" value="second_checkbox"/>&nbsp;&nbsp;<span id="checkBoxLabel">Include plenary sessions in schedule</span>
            <br/>
            <a href="#" id="generatePDFButton" class="btn btn--info btn--large">Download PDF</a>
        </div>
    </div>
</div>