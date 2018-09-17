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
<div class="day" id="day-3">Friday, 2 November, 2018</div>
    <div class="session session-plenary" id="session-welcome">
        <span class="session-title">Opening remarks</span>
        <br/>
        <span class="session-time">09:00 &ndash; 09:30</span>
        <br/>
        <span class="session-location btn btn--info btn--location">Gold Hall</span>
    </div>
    <div class="session session-expandable session-plenary">
        <div id="expander"></div>
        <a href="#" class="session-title">Keynote I: "Truth or Lie? Spoken Indicators of Deception in Speech"</a>
        <br/>
        <span class="session-people">Julia Hirschberg (Columbia University)</span>
        <br/>
        <span class="session-time">09:30 &ndash; 10:30</span>
        <br/>
        <span class="session-location btn btn--info btn--location">Gold Hall</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>Detecting deception from various forms of human behavior is a longstanding research goal which is of considerable interest to the military, law enforcement, corporate security, social services and mental health workers. However, both humans and polygraphs are very poor at this task. We describe more accurate methods we have developed to detect deception automatically from spoken language. Our classifiers are trained on the largest cleanly recorded corpus of within-subject deceptive and non-deceptive speech that has been collected. To distinguish truth from lie we make use of acoustic-prosodic, lexical, demographic, and personality features. We further examine differences in deceptive behavior based upon gender, personality, and native language (Mandarin Chinese vs. English), comparing our systems to human performance. We extend our studies to identify cues in trusted speech vs. mistrusted speech and how these features differ by speaker and by listener. Why does a listener believe a lie?</p>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-1">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">10:30 &ndash; 11:00</span>
    </div>
    <div class="session-box" id="session-box-1">
        <div class="session-header" id="session-header-1">Long Papers &amp; Demos I (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-1a">
            <div id="expander"></div>
            <a href="#" class="session-title">1A: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-1a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-1a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="1">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-001.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-002.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="3">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-003.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="4">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-004.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="5">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-005.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-1b">
            <div id="expander"></div>
            <a href="#" class="session-title">1B: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-1b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-1b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="6">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-006.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="7">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-007.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="8">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-008.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="9">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-009.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="10">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-010.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-1c">
            <div id="expander"></div>
            <a href="#" class="session-title">1C: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-1c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-1c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="11">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-011.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="12">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-012.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="13">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-013.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="14">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-014.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="15">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-015.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-1d">
            <div id="expander"></div>
            <a href="#" class="session-title">1D: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-1d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-1d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="16">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-016.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="17">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-017.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="18">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-018.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="19">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-019.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="20">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-020.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-1">
            <div id="expander"></div>
            <a href="#" class="session-title">1E: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="1">
                        <td>
                            <span class="poster-title">TITLE-021.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="2">
                        <td>
                            <span class="poster-title">TITLE-022.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-3">
        <span class="session-title">Lunch</span>
        <br/>
        <span class="session-time">12:30 &ndash; 13:45</span>
    </div>
    <div class="session-box" id="session-box-2">
        <div class="session-header" id="session-header-2">Short Papers I (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-2a">
            <div id="expander"></div>
            <a href="#" class="session-title">2A: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-2a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-2a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="21">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">TITLE-023.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="22">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">TITLE-024.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="23">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">TITLE-025.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="24">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">TITLE-026.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="25">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">TITLE-027.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-2b">
            <div id="expander"></div>
            <a href="#" class="session-title">2B: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-2b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-2b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="26">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">TITLE-028.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="27">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">TITLE-029.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="28">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">TITLE-030.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="29">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">TITLE-031.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="30">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">TITLE-032.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-2c">
            <div id="expander"></div>
            <a href="#" class="session-title">2C: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-2c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-2c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="31">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">TITLE-033.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="32">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">TITLE-034.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="33">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">TITLE-035.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="34">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">TITLE-036.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="35">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">TITLE-037.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-2d">
            <div id="expander"></div>
            <a href="#" class="session-title">2D: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-2d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-2d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="36">
                        <td id="paper-time">13:45&ndash;13:57</td>
                        <td>
                            <span class="paper-title">TITLE-038.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="37">
                        <td id="paper-time">13:57&ndash;14:09</td>
                        <td>
                            <span class="paper-title">TITLE-039.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="38">
                        <td id="paper-time">14:09&ndash;14:21</td>
                        <td>
                            <span class="paper-title">TITLE-040.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="39">
                        <td id="paper-time">14:21&ndash;14:33</td>
                        <td>
                            <span class="paper-title">TITLE-041.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="40">
                        <td id="paper-time">14:33&ndash;14:45</td>
                        <td>
                            <span class="paper-title">TITLE-042.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-2">
            <div id="expander"></div>
            <a href="#" class="session-title">2E: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="3">
                        <td>
                            <span class="poster-title">TITLE-043.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="4">
                        <td>
                            <span class="poster-title">TITLE-044.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-2">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">14:45 &ndash; 15:00</span>
    </div>
    <div class="session-box" id="session-box-3">
        <div class="session-header" id="session-header-3">Short Papers II (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-3a">
            <div id="expander"></div>
            <a href="#" class="session-title">3A: TBD</a>
            <br/>
            <span class="session-time">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-3a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-3a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="41">
                        <td id="paper-time">15:00&ndash;15:12</td>
                        <td>
                            <span class="paper-title">TITLE-045.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="42">
                        <td id="paper-time">15:12&ndash;15:24</td>
                        <td>
                            <span class="paper-title">TITLE-046.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="43">
                        <td id="paper-time">15:24&ndash;15:36</td>
                        <td>
                            <span class="paper-title">TITLE-047.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="44">
                        <td id="paper-time">15:36&ndash;15:48</td>
                        <td>
                            <span class="paper-title">TITLE-048.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="45">
                        <td id="paper-time">15:48&ndash;16:00</td>
                        <td>
                            <span class="paper-title">TITLE-049.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-3b">
            <div id="expander"></div>
            <a href="#" class="session-title">3B: TBD</a>
            <br/>
            <span class="session-time">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-3b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-3b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="46">
                        <td id="paper-time">15:00&ndash;15:12</td>
                        <td>
                            <span class="paper-title">TITLE-050.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="47">
                        <td id="paper-time">15:12&ndash;15:24</td>
                        <td>
                            <span class="paper-title">TITLE-051.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="48">
                        <td id="paper-time">15:24&ndash;15:36</td>
                        <td>
                            <span class="paper-title">TITLE-052.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="49">
                        <td id="paper-time">15:36&ndash;15:48</td>
                        <td>
                            <span class="paper-title">TITLE-053.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="50">
                        <td id="paper-time">15:48&ndash;16:00</td>
                        <td>
                            <span class="paper-title">TITLE-054.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-3c">
            <div id="expander"></div>
            <a href="#" class="session-title">3C: TBD</a>
            <br/>
            <span class="session-time">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-3c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-3c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="51">
                        <td id="paper-time">15:00&ndash;15:12</td>
                        <td>
                            <span class="paper-title">TITLE-055.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="52">
                        <td id="paper-time">15:12&ndash;15:24</td>
                        <td>
                            <span class="paper-title">TITLE-056.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="53">
                        <td id="paper-time">15:24&ndash;15:36</td>
                        <td>
                            <span class="paper-title">TITLE-057.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="54">
                        <td id="paper-time">15:36&ndash;15:48</td>
                        <td>
                            <span class="paper-title">TITLE-058.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="55">
                        <td id="paper-time">15:48&ndash;16:00</td>
                        <td>
                            <span class="paper-title">TITLE-059.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-3d">
            <div id="expander"></div>
            <a href="#" class="session-title">3D: TBD</a>
            <br/>
            <span class="session-time">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-3d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-3d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="56">
                        <td id="paper-time">15:00&ndash;15:12</td>
                        <td>
                            <span class="paper-title">TITLE-060.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="57">
                        <td id="paper-time">15:12&ndash;15:24</td>
                        <td>
                            <span class="paper-title">TITLE-061.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="58">
                        <td id="paper-time">15:24&ndash;15:36</td>
                        <td>
                            <span class="paper-title">TITLE-062.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="59">
                        <td id="paper-time">15:36&ndash;15:48</td>
                        <td>
                            <span class="paper-title">TITLE-063.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="60">
                        <td id="paper-time">15:48&ndash;16:00</td>
                        <td>
                            <span class="paper-title">TITLE-064.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-3">
            <div id="expander"></div>
            <a href="#" class="session-title">3E: TBD</a>
            <br/>
            <span class="session-time">15:00 &ndash; 16:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="5">
                        <td>
                            <span class="poster-title">TITLE-065.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="6">
                        <td>
                            <span class="poster-title">TITLE-066.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-3">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">16:00 &ndash; 16:30</span>
    </div>
    <div class="session-box" id="session-box-4">
        <div class="session-header" id="session-header-4">Long Papers &amp; Demos II (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-4a">
            <div id="expander"></div>
            <a href="#" class="session-title">4A: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-4a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-4a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="61">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">TITLE-067.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="62">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">TITLE-068.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="63">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">TITLE-069.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="64">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TITLE-070.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="65">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">TITLE-071.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-4b">
            <div id="expander"></div>
            <a href="#" class="session-title">4B: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-4b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-4b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="66">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">TITLE-072.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="67">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">TITLE-073.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="68">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">TITLE-074.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="69">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TITLE-075.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="70">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">TITLE-076.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-4c">
            <div id="expander"></div>
            <a href="#" class="session-title">4C: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-4c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-4c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="71">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">TITLE-077.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="72">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">TITLE-078.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="73">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">TITLE-079.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="74">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TITLE-080.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="75">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">TITLE-081.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-4d">
            <div id="expander"></div>
            <a href="#" class="session-title">4D: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-4d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-4d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="76">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">TITLE-082.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="77">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">TITLE-083.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="78">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">TITLE-084.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="79">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TITLE-085.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="80">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">TITLE-086.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-4">
            <div id="expander"></div>
            <a href="#" class="session-title">4E: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="7">
                        <td>
                            <span class="poster-title">TITLE-087.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="8">
                        <td>
                            <span class="poster-title">TITLE-088.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="day" id="day-4">Saturday, 3 November, 2018</div>
    <div class="session-box" id="session-box-5">
        <div class="session-header" id="session-header-5">Long Papers &amp; Demos III (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-5a">
            <div id="expander"></div>
            <a href="#" class="session-title">5A: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-5a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-5a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="81">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">TITLE-089.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="82">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">TITLE-090.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="83">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">TITLE-091.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="84">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">TITLE-092.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="85">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">TITLE-093.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-5b">
            <div id="expander"></div>
            <a href="#" class="session-title">5B: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-5b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-5b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="86">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">TITLE-094.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="87">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">TITLE-095.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="88">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">TITLE-096.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="89">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">TITLE-097.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="90">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">TITLE-098.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-5c">
            <div id="expander"></div>
            <a href="#" class="session-title">5C: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-5c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-5c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="91">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">TITLE-099.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="92">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">TITLE-100.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="93">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">TITLE-101.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="94">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">TITLE-102.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="95">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">TITLE-103.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-5d">
            <div id="expander"></div>
            <a href="#" class="session-title">5D: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-5d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-5d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="96">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">TITLE-104.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="97">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">TITLE-105.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="98">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">TITLE-106.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="99">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">TITLE-107.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="100">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">TITLE-108.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-5">
            <div id="expander"></div>
            <a href="#" class="session-title">5E: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="9">
                        <td>
                            <span class="poster-title">TITLE-109.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="10">
                        <td>
                            <span class="poster-title">TITLE-110.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-4">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">10:30 &ndash; 11:00</span>
    </div>
    <div class="session-box" id="session-box-6">
        <div class="session-header" id="session-header-6">Long Papers &amp; Demos IV (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-6a">
            <div id="expander"></div>
            <a href="#" class="session-title">6A: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-6a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-6a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="101">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-111.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="102">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-112.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="103">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-113.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="104">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-114.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="105">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-115.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-6b">
            <div id="expander"></div>
            <a href="#" class="session-title">6B: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-6b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-6b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="106">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-116.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="107">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-117.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="108">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-118.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="109">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-119.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="110">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-120.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-6c">
            <div id="expander"></div>
            <a href="#" class="session-title">6C: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-6c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-6c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="111">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-121.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="112">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-122.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="113">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-123.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="114">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-124.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="115">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-125.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-6d">
            <div id="expander"></div>
            <a href="#" class="session-title">6D: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-6d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-6d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="116">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-126.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="117">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-127.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="118">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-128.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="119">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-129.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="120">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-130.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-6">
            <div id="expander"></div>
            <a href="#" class="session-title">6E: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="11">
                        <td>
                            <span class="poster-title">TITLE-131.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="12">
                        <td>
                            <span class="poster-title">TITLE-132.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-4">
        <span class="session-title">Lunch</span>
        <br/>
        <span class="session-time">12:30 &ndash; 13:45</span>
    </div>
    <div class="session-box" id="session-box-7">
        <div class="session-header" id="session-header-7">Short Papers III (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-7a">
            <div id="expander"></div>
            <a href="#" class="session-title">7A: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-7a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-7a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="121">
                        <td id="paper-time">14:45&ndash;14:57</td>
                        <td>
                            <span class="paper-title">TITLE-133.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="122">
                        <td id="paper-time">14:57&ndash;15:09</td>
                        <td>
                            <span class="paper-title">TITLE-134.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="123">
                        <td id="paper-time">15:09&ndash;15:21</td>
                        <td>
                            <span class="paper-title">TITLE-135.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="124">
                        <td id="paper-time">15:21&ndash;15:33</td>
                        <td>
                            <span class="paper-title">TITLE-136.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="125">
                        <td id="paper-time">15:33&ndash;15:45</td>
                        <td>
                            <span class="paper-title">TITLE-137.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-7b">
            <div id="expander"></div>
            <a href="#" class="session-title">7B: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-7b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-7b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="126">
                        <td id="paper-time">14:45&ndash;14:57</td>
                        <td>
                            <span class="paper-title">TITLE-138.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="127">
                        <td id="paper-time">14:57&ndash;15:09</td>
                        <td>
                            <span class="paper-title">TITLE-139.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="128">
                        <td id="paper-time">15:09&ndash;15:21</td>
                        <td>
                            <span class="paper-title">TITLE-140.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="129">
                        <td id="paper-time">15:21&ndash;15:33</td>
                        <td>
                            <span class="paper-title">TITLE-141.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="130">
                        <td id="paper-time">15:33&ndash;15:45</td>
                        <td>
                            <span class="paper-title">TITLE-142.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-7c">
            <div id="expander"></div>
            <a href="#" class="session-title">7C: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-7c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-7c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="131">
                        <td id="paper-time">14:45&ndash;14:57</td>
                        <td>
                            <span class="paper-title">TITLE-143.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="132">
                        <td id="paper-time">14:57&ndash;15:09</td>
                        <td>
                            <span class="paper-title">TITLE-144.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="133">
                        <td id="paper-time">15:09&ndash;15:21</td>
                        <td>
                            <span class="paper-title">TITLE-145.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="134">
                        <td id="paper-time">15:21&ndash;15:33</td>
                        <td>
                            <span class="paper-title">TITLE-146.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="135">
                        <td id="paper-time">15:33&ndash;15:45</td>
                        <td>
                            <span class="paper-title">TITLE-147.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-7d">
            <div id="expander"></div>
            <a href="#" class="session-title">7D: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-7d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-7d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="136">
                        <td id="paper-time">14:45&ndash;14:57</td>
                        <td>
                            <span class="paper-title">TITLE-148.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="137">
                        <td id="paper-time">14:57&ndash;15:09</td>
                        <td>
                            <span class="paper-title">TITLE-149.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="138">
                        <td id="paper-time">15:09&ndash;15:21</td>
                        <td>
                            <span class="paper-title">TITLE-150.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="139">
                        <td id="paper-time">15:21&ndash;15:33</td>
                        <td>
                            <span class="paper-title">TITLE-151.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="140">
                        <td id="paper-time">15:33&ndash;15:45</td>
                        <td>
                            <span class="paper-title">TITLE-152.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-7">
            <div id="expander"></div>
            <a href="#" class="session-title">7E: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="13">
                        <td>
                            <span class="poster-title">TITLE-153.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="14">
                        <td>
                            <span class="poster-title">TITLE-154.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-5">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">14:45 &ndash; 15:00</span>
    </div>
    <div class="session session-expandable session-plenary">
        <div id="expander"></div>
        <a href="#" class="session-title">Keynote II: "Understanding the News that Moves Markets"</a>
        <br/>
        <span class="session-people">Gideon Mann (Bloomberg, L.P.)</span>
        <br/>
        <span class="session-time">15:00 &ndash; 16:00</span>
        <br/>
        <span class="session-location btn btn--info btn--location">Gold Hall</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>Since the dawn of human civilization, finance and language technology have been connected. However, only recently have advances in statistical language understanding, and an ever-increasing thirst for market advantage, led to the widespread application of natural language technology across the global capital markets. This talk will review the ways in which language technology is enabling market participants to quickly understand and respond to major world events and breaking business news. It will outline the state of the art in applications of NLP to finance and highlight open problems that are being addressed by emerging research.</p>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-6">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">16:00 &ndash; 16:30</span>
    </div>
    <div class="session-box" id="session-box-8">
        <div class="session-header" id="session-header-8">Long Papers &amp; Demos V (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-8a">
            <div id="expander"></div>
            <a href="#" class="session-title">8A: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-8a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-8a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="141">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">TITLE-155.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="142">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">TITLE-156.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="143">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">TITLE-157.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="144">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TITLE-158.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="145">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">TITLE-159.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-8b">
            <div id="expander"></div>
            <a href="#" class="session-title">8B: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-8b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-8b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="146">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">TITLE-160.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="147">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">TITLE-161.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="148">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">TITLE-162.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="149">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TITLE-163.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="150">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">TITLE-164.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-8c">
            <div id="expander"></div>
            <a href="#" class="session-title">8C: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-8c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-8c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="151">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">TITLE-165.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="152">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">TITLE-166.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="153">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">TITLE-167.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="154">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TITLE-168.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="155">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">TITLE-169.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-8d">
            <div id="expander"></div>
            <a href="#" class="session-title">8D: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-8d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-8d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="156">
                        <td id="paper-time">16:30&ndash;16:48</td>
                        <td>
                            <span class="paper-title">TITLE-170.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="157">
                        <td id="paper-time">16:48&ndash;17:06</td>
                        <td>
                            <span class="paper-title">TITLE-171.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="158">
                        <td id="paper-time">17:06&ndash;17:24</td>
                        <td>
                            <span class="paper-title">TITLE-172.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="159">
                        <td id="paper-time">17:24&ndash;17:42</td>
                        <td>
                            <span class="paper-title">TITLE-173.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="160">
                        <td id="paper-time">17:42&ndash;18:00</td>
                        <td>
                            <span class="paper-title">TITLE-174.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-8">
            <div id="expander"></div>
            <a href="#" class="session-title">8E: TBD</a>
            <br/>
            <span class="session-time">16:30 &ndash; 18:00</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="15">
                        <td>
                            <span class="poster-title">TITLE-175.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="16">
                        <td>
                            <span class="poster-title">TITLE-176.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="day" id="day-5">Sunday, 4 November, 2018</div>
    <div class="session-box" id="session-box-9">
        <div class="session-header" id="session-header-9">Long Papers &amp; Demos VI (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-9a">
            <div id="expander"></div>
            <a href="#" class="session-title">9A: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-9a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-9a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="161">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">TITLE-177.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="162">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">TITLE-178.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="163">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">TITLE-179.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="164">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">TITLE-180.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="165">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">TITLE-181.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-9b">
            <div id="expander"></div>
            <a href="#" class="session-title">9B: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-9b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-9b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="166">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">TITLE-182.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="167">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">TITLE-183.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="168">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">TITLE-184.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="169">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">TITLE-185.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="170">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">TITLE-186.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-9c">
            <div id="expander"></div>
            <a href="#" class="session-title">9C: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-9c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-9c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="171">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">TITLE-187.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="172">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">TITLE-188.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="173">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">TITLE-189.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="174">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">TITLE-190.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="175">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">TITLE-191.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-9d">
            <div id="expander"></div>
            <a href="#" class="session-title">9D: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-9d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-9d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="176">
                        <td id="paper-time">09:00&ndash;09:18</td>
                        <td>
                            <span class="paper-title">TITLE-192.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="177">
                        <td id="paper-time">09:18&ndash;09:36</td>
                        <td>
                            <span class="paper-title">TITLE-193.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="178">
                        <td id="paper-time">09:36&ndash;09:54</td>
                        <td>
                            <span class="paper-title">TITLE-194.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="179">
                        <td id="paper-time">09:54&ndash;10:12</td>
                        <td>
                            <span class="paper-title">TITLE-195.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="180">
                        <td id="paper-time">10:12&ndash;10:30</td>
                        <td>
                            <span class="paper-title">TITLE-196.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-9">
            <div id="expander"></div>
            <a href="#" class="session-title">9E: TBD</a>
            <br/>
            <span class="session-time">09:00 &ndash; 09:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="17">
                        <td>
                            <span class="poster-title">TITLE-197.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="18">
                        <td>
                            <span class="poster-title">TITLE-198.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-7">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">10:30 &ndash; 11:00</span>
    </div>
    <div class="session-box" id="session-box-10">
        <div class="session-header" id="session-header-10">Long Papers &amp; Demos VII (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-10a">
            <div id="expander"></div>
            <a href="#" class="session-title">10A: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-10a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-10a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="181">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-199.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="182">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-200.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="183">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-201.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="184">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-202.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="185">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-203.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-10b">
            <div id="expander"></div>
            <a href="#" class="session-title">10B: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-10b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-10b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="186">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-204.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="187">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-205.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="188">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-206.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="189">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-207.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="190">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-208.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-10c">
            <div id="expander"></div>
            <a href="#" class="session-title">10C: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-10c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-10c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="191">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-209.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="192">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-210.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="193">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-211.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="194">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-212.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="195">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-213.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-10d">
            <div id="expander"></div>
            <a href="#" class="session-title">10D: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-10d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-10d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="196">
                        <td id="paper-time">11:00&ndash;11:18</td>
                        <td>
                            <span class="paper-title">TITLE-214.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="197">
                        <td id="paper-time">11:18&ndash;11:36</td>
                        <td>
                            <span class="paper-title">TITLE-215.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="198">
                        <td id="paper-time">11:36&ndash;11:54</td>
                        <td>
                            <span class="paper-title">TITLE-216.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="199">
                        <td id="paper-time">11:54&ndash;12:12</td>
                        <td>
                            <span class="paper-title">TITLE-217.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="200">
                        <td id="paper-time">12:12&ndash;12:30</td>
                        <td>
                            <span class="paper-title">TITLE-218.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-10">
            <div id="expander"></div>
            <a href="#" class="session-title">10E: TBD</a>
            <br/>
            <span class="session-time">11:00 &ndash; 12:30</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="19">
                        <td>
                            <span class="poster-title">TITLE-219.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="20">
                        <td>
                            <span class="poster-title">TITLE-220.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-lunch-5">
        <span class="session-title">Lunch</span>
        <br/>
        <span class="session-time">12:30 &ndash; 13:45</span>
    </div>
    <div class="session-box" id="session-box-11">
        <div class="session-header" id="session-header-11">Short Papers IV (Orals &amp; Posters)</div>
        <div class="session session-expandable session-papers1" id="session-11a">
            <div id="expander"></div>
            <a href="#" class="session-title">11A: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-11a-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-11a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="201">
                        <td id="paper-time">14:45&ndash;14:57</td>
                        <td>
                            <span class="paper-title">TITLE-221.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="202">
                        <td id="paper-time">14:57&ndash;15:09</td>
                        <td>
                            <span class="paper-title">TITLE-222.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="203">
                        <td id="paper-time">15:09&ndash;15:21</td>
                        <td>
                            <span class="paper-title">TITLE-223.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="204">
                        <td id="paper-time">15:21&ndash;15:33</td>
                        <td>
                            <span class="paper-title">TITLE-224.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="205">
                        <td id="paper-time">15:33&ndash;15:45</td>
                        <td>
                            <span class="paper-title">TITLE-225.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers2" id="session-11b">
            <div id="expander"></div>
            <a href="#" class="session-title">11B: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-11b-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-11b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="206">
                        <td id="paper-time">14:45&ndash;14:57</td>
                        <td>
                            <span class="paper-title">TITLE-226.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="207">
                        <td id="paper-time">14:57&ndash;15:09</td>
                        <td>
                            <span class="paper-title">TITLE-227.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="208">
                        <td id="paper-time">15:09&ndash;15:21</td>
                        <td>
                            <span class="paper-title">TITLE-228.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="209">
                        <td id="paper-time">15:21&ndash;15:33</td>
                        <td>
                            <span class="paper-title">TITLE-229.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="210">
                        <td id="paper-time">15:33&ndash;15:45</td>
                        <td>
                            <span class="paper-title">TITLE-230.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers3" id="session-11c">
            <div id="expander"></div>
            <a href="#" class="session-title">11C: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-11c-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-11c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="211">
                        <td id="paper-time">14:45&ndash;14:57</td>
                        <td>
                            <span class="paper-title">TITLE-231.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="212">
                        <td id="paper-time">14:57&ndash;15:09</td>
                        <td>
                            <span class="paper-title">TITLE-232.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="213">
                        <td id="paper-time">15:09&ndash;15:21</td>
                        <td>
                            <span class="paper-title">TITLE-233.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="214">
                        <td id="paper-time">15:21&ndash;15:33</td>
                        <td>
                            <span class="paper-title">TITLE-234.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="215">
                        <td id="paper-time">15:33&ndash;15:45</td>
                        <td>
                            <span class="paper-title">TITLE-235.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-papers4" id="session-11d">
            <div id="expander"></div>
            <a href="#" class="session-title">11D: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Gold Hall</span>
            <br/>
            <div class="paper-session-details">
                <br/>
                <a href="#" class="session-selector" id="session-11d-selector">Choose All</a>
                <a href="#" class="session-deselector" id="session-11d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td class="session-chair" colspan="2">Chair: TBD</td>
                    </tr>
                    <tr id="paper" paper-id="216">
                        <td id="paper-time">14:45&ndash;14:57</td>
                        <td>
                            <span class="paper-title">TITLE-236.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="217">
                        <td id="paper-time">14:57&ndash;15:09</td>
                        <td>
                            <span class="paper-title">TITLE-237.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="218">
                        <td id="paper-time">15:09&ndash;15:21</td>
                        <td>
                            <span class="paper-title">TITLE-238.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="219">
                        <td id="paper-time">15:21&ndash;15:33</td>
                        <td>
                            <span class="paper-title">TITLE-239.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="220">
                        <td id="paper-time">15:33&ndash;15:45</td>
                        <td>
                            <span class="paper-title">TITLE-240.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="session session-expandable session-posters" id="session-poster-11">
            <div id="expander"></div>
            <a href="#" class="session-title">11E: TBD</a>
            <br/>
            <span class="session-time">13:45 &ndash; 14:45</span>
            <br/>
            <span class="session-location btn btn--info btn--location">Grand Hall 2</span>
            <div class="poster-session-details">
                <br/>
                <table class="poster-table">
                    <tr id="poster" poster-id="21">
                        <td>
                            <span class="poster-title">TITLE-241.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                    <tr id="poster" poster-id="22">
                        <td>
                            <span class="poster-title">TITLE-242.</span>
                            <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-8">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">14:45 &ndash; 15:00</span>
    </div>
    <div class="session session-expandable session-plenary">
        <div id="expander"></div>
        <a href="#" class="session-title">Keynote III: "The Moment of Meaning and the Future of Computational Semantics"</a>
        <br/>
        <span class="session-people">Johan Bos (University of Groningen)</span>
        <br/>
        <span class="session-time">15:00 &ndash; 16:00</span>
        <br/>
        <span class="session-location btn btn--info btn--location">Gold Hall</span>
        <div class="paper-session-details">
            <br/>
            <div class="session-abstract">
                <p>There are many recent advances in semantic parsing: we see a rising number of semantically annotated corpora and there is exciting technology (such as neural networks) to be explored. In this talk I will discuss what role computational semantics could play in future natural language processing applications (including fact checking and machine translation). I will argue that we should not just look at semantic parsing, but that things can get really interesting when we can use language-neutral meaning representations to draw (transparent) inferences. The main ideas will be exemplified by the parallel meaning bank, a new corpus comprising texts annotated with formal meaning representations for English, Dutch, German and Italian.</p>
            </div>
        </div>
    </div>
    <div class="session session-break session-plenary" id="session-break-9">
        <span class="session-title">Coffee Break</span>
        <br/>
        <span class="session-time">16:00 &ndash; 16:30</span>
    </div>
    <div class="session session-expandable session-papers-best">
        <div id="expander"></div>
        <a href="#" class="session-title">Best Paper Awards and Closing</a>
        <br/>
        <span class="session-time">16:30 &ndash; 18:00</span>
        <br/>
        <span class="session-location btn btn--info btn--location">Gold Hall</span>
        <br/>
        <div class="paper-session-details">
            <br/>
            <table class="paper-table">
                <tr id="best-paper" paper-id="ID">
                    <td id="paper-time">16:30&ndash;16:42</td>
                    <td>
                        <span class="paper-title">TITLE.</span>
                        <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>&nbsp;(short)
                    </td>
                </tr>
                <tr id="best-paper" paper-id="ID">
                    <td id="paper-time">16:42&ndash;17:00</td>
                    <td>
                        <span class="paper-title">TITLE.</span>
                        <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>&nbsp;(long)
                    </td>
                </tr>
                <tr id="best-paper" paper-id="ID">
                    <td id="paper-time">17:00&ndash;17:18</td>
                    <td>
                        <span class="paper-title">TITLE.</span>
                        <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>&nbsp;(long)
                    </td>
                </tr>
                <tr id="best-paper" paper-id="ID">
                    <td id="paper-time">17:18&ndash;17:36</td>
                    <td>
                        <span class="paper-title">TITLE.</span>
                        <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>&nbsp;(long)
                    </td>
                </tr>
                <tr id="best-paper" paper-id="ID">
                    <td id="paper-time">17:36&ndash;17:54</td>
                    <td>
                        <span class="paper-title">TITLE.</span>
                        <em>AUTHOR1, AUTHOR2, and AUTHOR3</em>&nbsp;(long)
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <div id="generatePDFForm">
        <div id="formContainer">
            <input type="checkbox" id="includePlenaryCheckBox" value="second_checkbox"/>&nbsp;&nbsp;<span id="checkBoxLabel">Include plenary sessions in schedule</span>
            <br/>
            <a href="#" id="generatePDFButton" class="btn btn--info btn--large">Download PDF</a>
        </div>
    </div>
</div>