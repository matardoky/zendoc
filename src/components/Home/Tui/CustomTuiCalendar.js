import React, {
  useRef,
  useLayoutEffect,
  useEffect,
  forwardRef,
  useImperativeHandle,
  useState
} from 'react'

import TuiCalendar from "tui-calendar"
import moment from 'moment'

const CustomTuiCalendar = forwardRef(
  (
    {
      height = "800px",
      defaultView = "week",
      calendars = [],
      schedules = [], 
      isReadOnly = true,
      showSlidebar = false,
      showMenu = false,
      onCreate, 
      createText = "New schedule",
      onBeforeCreateSchedule = () => false,
      onBeforeUpdateSchedule = () => false,
      onBeforeDeleteSchedule = () => false,
      ...rest
    },
    ref
  ) => {
      const calendarInstRef = useRef(null)
      const tuiRef = useRef(null)
      const wrapperRef = useRef(null)
      const [open, setOpen] = useState(false)
      const [renderRange, setRenderRange] = useState("")
      const [workweek, setWorkweek] = useState(true)
      const [narrowWeekend, setNarrowWeekend] = useState(true)
      const [startDayOfWeek, setStartDayOfWeek] = useState(1)
      const [type, setType] = useState("weekly")
      const [checkedCalendars,setCheckedCalendars ] = useState(
          calendars.map((element) => ({...element, isChecked:true}))
      )
      const [filterSchedules, setFilterSchedules] = useState(schedules)
 
    useImperativeHandle(ref, ()=> ({
        getAlert(){
            alert("getAlert from child")
        }, 
        createSchedule, 
        updateSchedule,
        deleteSchedule
    }))
 
    useEffect(()=>{
      calendarInstRef.current = new TuiCalendar(tuiRef.current, {
        useDetailPopup:false, 
        useCreationPopup:false, 
        template:{
            timegridDisplayPrimayTime: function (time) {
              return (time.hour < 10 ? '0' : '') + time.hour + ':' + time.minutes + '0';
            },
            timegridDisplayTime: function (time) {
              return (time.hour < 10 ? '0' : '') + time.hour + ':' + time.minutes + '0';
            },
        },
        calendars,
        ...rest
      })
      setRenderRangeText()
      
      calendarInstRef.current.clear()
      calendarInstRef.current.createSchedules(filterSchedules, true)
      calendarInstRef.current.render()

      calendarInstRef.current.on("beforeCreateSchedule", function(event){
        onBeforeCreateSchedule(event)
      })

      calendarInstRef.current.on("beforeUpdateSchedule", function(event){
        onBeforeUpdateSchedule(event)
      })

      calendarInstRef.current.on("beforeDeleteSchedule", function(event){
        onBeforeDeleteSchedule(event)
      })

      calendarInstRef.current.on("clickSchedule", function (event) {
        // var schedule = event.schedule;
        // console.log("clickSchedule", event);
        // if (lastClickSchedule) {
        //   calendarInstRef.current.updateSchedule(
        //     lastClickSchedule.id,
        //     lastClickSchedule.calendarId,
        //     {
        //       isFocused: false
        //     }
        //   );
        // }
        // calendarInstRef.current.updateSchedule(schedule.id, schedule.calendarId, {
        //   isFocused: true
        // });
        // lastClickSchedule = schedule;
        // open detail view
      });

      calendarInstRef.current.on("clickDayname", function (event) {
        // console.log("clickDayname", event);
        if (calendarInstRef.current.getViewName() === "week") {
          calendarInstRef.current.setDate(new Date(event.date));
          calendarInstRef.current.changeView("day", true);
        }
      });

      calendarInstRef.current.on("clickMore", function (event) {
        // console.log("clickMore", event.date, event.target);
      });

      calendarInstRef.current.on("clickTimezonesCollapseBtn", function (
        timezonesCollapsed
      ) {
        // console.log(timezonesCollapsed);
      });

      calendarInstRef.current.on("afterRenderSchedule", function (event) {
        // var schedule = event.schedule;
        // var element = calendarInstRef.current.getElement(
        //   schedule.id,
        //   schedule.calendarId
        // );
        // use the element
        // console.log(element);
      });
      return () => {
        calendarInstRef.current.destroy();
      };

    }, [tuiRef, schedules])

    useLayoutEffect(() => {
      // console.log("before render");
    });

    function currentCalendarDate(format) {
      var currentDate = moment([
        calendarInstRef.current.getDate().getFullYear(),
        calendarInstRef.current.getDate().getMonth(),
        calendarInstRef.current.getDate().getDate()
      ]);

      return currentDate.format(format);
    }
    
    function setRenderRangeText() {
      var options = calendarInstRef.current.getOptions();
      var viewName = calendarInstRef.current.getViewName();

      var html = [];
      if (viewName === "day") {
        html.push(currentCalendarDate("YYYY.MM.DD"));
      } else if (
        viewName === "month" &&
        (!options.month.visibleWeeksCount ||
          options.month.visibleWeeksCount > 4)
      ) {
        html.push(currentCalendarDate("YYYY.MM"));
      } else {
        html.push(
          moment(calendarInstRef.current.getDateRangeStart().getTime()).format(
            "YYYY.MM.DD"
          )
        );
        html.push(" ~ ");
        html.push(
          moment(calendarInstRef.current.getDateRangeEnd().getTime()).format(
            " MM.DD"
          )
        );
      }
      setRenderRange(html.join(""));
    }

    function _getTimeTemplate(schedule, isAllDay) {
      var html = [];

      if (!isAllDay) {
        html.push(
          "<strong>" +
            moment(schedule.start.toDate()).format("HH:mm") +
            "</strong> "
        );
      }
      if (schedule.isPrivate) {
        html.push('<span class="calendar-font-icon ic-lock-b"></span>');
        html.push(" Private");
      } else {
        if (schedule.isReadOnly) {
          html.push('<span class="calendar-font-icon ic-readonly-b"></span>');
        } else if (schedule.recurrenceRule) {
          html.push('<span class="calendar-font-icon ic-repeat-b"></span>');
        } else if (schedule.attendees.length) {
          html.push('<span class="calendar-font-icon ic-user-b"></span>');
        } else if (schedule.location) {
          html.push('<span class="calendar-font-icon ic-location-b"></span>');
        }

        html.push(" " + schedule.title);
      }

      return html.join("");
    }

    useEffect(() => {
      document.addEventListener("click", handleClick, false);

      return () => {
        document.removeEventListener("click", handleClick, false);
      };
    });

    const handleClick = (e) => {
      if (wrapperRef.current?.contains(e.target)) {
        // inside click
        // console.log("inside");
        return;
      }
      // outside click
      // ... do whatever on click outside here ...
      // console.log("outside");
      setOpen(false);
    };

    const handleAllChecked = (event) => {
      const cloneCheckedCalendars = [...checkedCalendars];
      cloneCheckedCalendars.forEach(
        (element) => (element.isChecked = event.target.checked)
      );
      setCheckedCalendars(cloneCheckedCalendars);
      filterCalendar(cloneCheckedCalendars);
    };

    const handleCheckChildElement = (event) => {
      const cloneCheckedCalendars = [...checkedCalendars];
      cloneCheckedCalendars.forEach((element) => {
        if (element.id === event.target.value)
          element.isChecked = event.target.checked;
      });
      setCheckedCalendars(cloneCheckedCalendars);
      filterCalendar(cloneCheckedCalendars);
    };

    const filterCalendar = (cloneCheckedCalendars) => {
      const filterCalendars = cloneCheckedCalendars
        .filter((element) => element.isChecked === false)
        .map((item) => item.id);
      const cloneSchedules = filterSchedules.filter((element) => {
        return filterCalendars.indexOf(element.calendarId) === -1;
      });

      // rerender
      calendarInstRef.current.clear();
      calendarInstRef.current.createSchedules(cloneSchedules, true);
      calendarInstRef.current.render();
    };

    function createSchedule(schedule) {
      console.log("createSchedule");

      calendarInstRef.current.createSchedules([schedule]);
      const cloneFilterSchedules = [...filterSchedules];
      setFilterSchedules((prevState) => [...cloneFilterSchedules, schedule]);
    }

    function updateSchedule(schedule, changes) {
      console.log("updateSchedule");

      calendarInstRef.current.updateSchedule(
        schedule.id,
        schedule.calendarId,
        changes
      );
      const cloneFilterSchedules = [...filterSchedules];
      setFilterSchedules((prevState) =>
        cloneFilterSchedules.map((item) => {
          if (item.id === schedule.id) {
            return { ...item, ...changes };
          }
          return item;
        })
      );
    }

    function deleteSchedule(schedule) {
      console.log("deleteSchedule");

      calendarInstRef.current.deleteSchedule(schedule.id, schedule.calendarId);
      const cloneFilterSchedules = [...filterSchedules];
      setFilterSchedules((prevState) =>
        cloneFilterSchedules.filter((item) => item.id !== schedule.id)
      );
    }

    return (
      <div>
        {showSlidebar && (
          <div id="lnb">
            {onCreate && (
              <div className="lnb-new-schedule">
                <button
                  id="btn-new-schedule"
                  type="button"
                  className="btn btn-default btn-block lnb-new-schedule-btn"
                  data-toggle="modal"
                  onClick={onCreate}
                >
                  {createText}
                </button>
              </div>
            )}
            <div id="lnb-calendars" className="lnb-calendars">
              <div>
                <div className="lnb-calendars-item">
                  <label>
                    <input
                      className="tui-full-calendar-checkbox-square"
                      type="checkbox"
                      defaultValue="all"
                      checked={checkedCalendars.every(
                        (element) => element.isChecked === true
                      )}
                      onChange={handleAllChecked}
                    />
                    <span />
                    <strong>View all</strong>
                  </label>
                </div>
              </div>
              <div id="calendarList" className="lnb-calendars-d1">
                {checkedCalendars.map((element, i) => {
                  return (
                    <div key={i} className="lnb-calendars-item">
                      <label>
                        <input
                          type="checkbox"
                          className="tui-full-calendar-checkbox-round"
                          defaultValue={element.id}
                          checked={element.isChecked}
                          onChange={handleCheckChildElement}
                        />
                        <span
                          style={{
                            borderColor: element.bgColor,
                            backgroundColor: element.isChecked
                              ? element.bgColor
                              : "transparent"
                          }}
                        />
                        <span>{element.name}</span>
                      </label>
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="lnb-footer">© NHN Corp.</div>
          </div>
        )}

        <div id="right" style={{ left: !showSlidebar && 0 }}>
          {showMenu && (
            <div id="menu">
              <span
                ref={wrapperRef}
                style={{ marginRight: "4px" }}
                className={`dropdown ${open && "open"}`}
              >
                <button
                  id="dropdownMenu-calendarType"
                  className="btn btn-default btn-sm dropdown-toggle"
                  type="button"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded={open}
                  onClick={() => setOpen(!open)}
                >
                  <i
                    id="calendarTypeIcon"
                    className="calendar-icon ic_view_week"
                    style={{ marginRight: "4px" }}
                  />
                  <span id="calendarTypeName">{type}</span>&nbsp;
                  <i className="calendar-icon tui-full-calendar-dropdown-arrow" />
                </button>
                <ul
                  className="dropdown-menu"
                  role="menu"
                  aria-labelledby="dropdownMenu-calendarType"
                >
                  <li role="presentation">
                    <a
                      href="/"
                      onClick={(e) => {
                        e.preventDefault();
                        calendarInstRef.current.changeView("day", true);
                        setType("Daily");
                        setOpen(false);
                      }}
                      className="dropdown-menu-title"
                      role="menuitem"
                      data-action="toggle-daily"
                    >
                      <i className="calendar-icon ic_view_day" />
                      Daily
                    </a>
                  </li>
                  <li role="presentation">
                    <a
                      href="/"
                      onClick={(e) => {
                        e.preventDefault();
                        calendarInstRef.current.changeView("week", true);
                        setType("Weekly");
                        setOpen(false);
                      }}
                      className="dropdown-menu-title"
                      role="menuitem"
                      data-action="toggle-weekly"
                    >
                      <i className="calendar-icon ic_view_week" />
                      Weekly
                    </a>
                  </li>
                  <li role="presentation">
                    <a
                      href="/"
                      onClick={(e) => {
                        e.preventDefault();
                        calendarInstRef.current.setOptions(
                          { month: { visibleWeeksCount: 6 } },
                          true
                        ); // or null
                        calendarInstRef.current.changeView("month", true);
                        setType("Month");
                        setOpen(false);
                      }}
                      className="dropdown-menu-title"
                      role="menuitem"
                      data-action="toggle-monthly"
                    >
                      <i className="calendar-icon ic_view_month" />
                      Month
                    </a>
                  </li>
                  <li role="presentation">
                    <a
                      href="/"
                      onClick={(e) => {
                        e.preventDefault();
                        calendarInstRef.current.setOptions(
                          { month: { visibleWeeksCount: 2 } },
                          true
                        ); // or null
                        calendarInstRef.current.changeView("month", true);
                        setType("2 weeks");
                        setOpen(false);
                      }}
                      className="dropdown-menu-title"
                      role="menuitem"
                      data-action="toggle-weeks2"
                    >
                      <i className="calendar-icon ic_view_week" />2 weeks
                    </a>
                  </li>
                  <li role="presentation">
                    <a
                      href="/"
                      onClick={(e) => {
                        e.preventDefault();
                        calendarInstRef.current.setOptions(
                          { month: { visibleWeeksCount: 3 } },
                          true
                        ); // or null
                        calendarInstRef.current.changeView("month", true);
                        setType("3 weeks");
                        setOpen(false);
                      }}
                      className="dropdown-menu-title"
                      role="menuitem"
                      data-action="toggle-weeks3"
                    >
                      <i className="calendar-icon ic_view_week" />3 weeks
                    </a>
                  </li>
                  <li role="presentation" className="dropdown-divider" />
                  <li role="presentation">
                    <a
                      href="/"
                      onClick={(e) => {
                        e.preventDefault();
                        calendarInstRef.current.setOptions(
                          { month: { workweek } },
                          true
                        );
                        calendarInstRef.current.setOptions(
                          { week: { workweek } },
                          true
                        );
                        calendarInstRef.current.changeView(
                          calendarInstRef.current.getViewName(),
                          true
                        );
                        setWorkweek(!workweek);
                        setOpen(false);
                      }}
                      role="menuitem"
                      data-action="toggle-workweek"
                    >
                      <input
                        type="checkbox"
                        className="tui-full-calendar-checkbox-square"
                        checked={workweek}
                        onChange={() => {}}
                      />
                      <span className="checkbox-title" />
                      Show weekends
                    </a>
                  </li>
                  <li role="presentation">
                    <a
                      href="/"
                      onClick={(e) => {
                        e.preventDefault();
                        calendarInstRef.current.setOptions(
                          { week: { startDayOfWeek } },
                          true
                        );
                        calendarInstRef.current.setOptions(
                          { month: { startDayOfWeek } },
                          true
                        );
                        calendarInstRef.current.changeView(
                          calendarInstRef.current.getViewName(),
                          true
                        );
                        setStartDayOfWeek(startDayOfWeek === 1 ? 0 : 1);
                        setOpen(false);
                      }}
                      role="menuitem"
                      data-action="toggle-start-day-1"
                    >
                      <input
                        type="checkbox"
                        className="tui-full-calendar-checkbox-square"
                        checked={startDayOfWeek !== 1 ? true : false}
                        onChange={() => {}}
                      />
                      <span className="checkbox-title" />
                      Start Week on Monday
                    </a>
                  </li>
                  <li role="presentation">
                    <a
                      href="/"
                      onClick={(e) => {
                        e.preventDefault();
                        calendarInstRef.current.setOptions(
                          { month: { narrowWeekend } },
                          true
                        );
                        calendarInstRef.current.setOptions(
                          { week: { narrowWeekend } },
                          true
                        );
                        calendarInstRef.current.changeView(
                          calendarInstRef.current.getViewName(),
                          true
                        );
                        setNarrowWeekend(!narrowWeekend);
                        setOpen(false);
                      }}
                      role="menuitem"
                      data-action="toggle-narrow-weekend"
                    >
                      <input
                        type="checkbox"
                        className="tui-full-calendar-checkbox-square"
                        checked={narrowWeekend}
                        onChange={() => {}}
                      />
                      <span className="checkbox-title" />
                      Narrower than weekdays
                    </a>
                  </li>
                </ul>
              </span>

              <span id="menu-navi">
                <button
                  type="button"
                  className="btn btn-default btn-sm move-today"
                  style={{ marginRight: "4px" }}
                  data-action="move-today"
                  onClick={() => {
                    // console.log("today");
                    calendarInstRef.current.today();
                    setRenderRangeText();
                  }}
                >
                  Today
                </button>
                <button
                  type="button"
                  className="btn btn-default btn-sm move-day"
                  style={{ marginRight: "4px" }}
                  data-action="move-prev"
                  onClick={() => {
                    // console.log("pre");
                    calendarInstRef.current.prev();
                    setRenderRangeText();
                  }}
                >
                  <i
                    className="calendar-icon ic-arrow-line-left"
                    data-action="move-prev"
                  />
                </button>
                <button
                  type="button"
                  className="btn btn-default btn-sm move-day"
                  style={{ marginRight: "4px" }}
                  data-action="move-next"
                  onClick={() => {
                    // console.log("next");
                    calendarInstRef.current.next();
                    setRenderRangeText();
                  }}
                >
                  <i
                    className="calendar-icon ic-arrow-line-right"
                    data-action="move-next"
                  />
                </button>
              </span>
              <span id="renderRange" className="render-range">
                {renderRange}
              </span>
            </div>
          )}
          <div ref={tuiRef} style={{ height }} />
        </div>
      </div>
    );

  }
)
export default CustomTuiCalendar
