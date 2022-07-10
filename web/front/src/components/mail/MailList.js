import React from "react";
import {
  AdaptivityProvider,
  ConfigProvider,
  Header,
  useAdaptivity,
  AppRoot,
  Avatar,
  SplitLayout,
  SplitCol,
  Button,
  ViewWidth,
  View,
  Panel,
  PanelHeader,
  List,
    Group,
  IconButton,
  PanelHeaderButton,
  Cell,
} from "@vkontakte/vkui";
import { Icon28MoonOutline } from '@vkontakte/icons';
import { MailItem } from "./MailItem"
import {
    Icon28Notifications
} from "@vkontakte/icons";
import styled from "styled-components"
import axios from "axios"
import { useEffect, useState } from "react";
import "@vkontakte/vkui/dist/vkui.css";

export function MailList() {
  const { viewWidth } = useAdaptivity();
  const [data, setData] = useState([])
  const [pagination, setPagination] = useState(1)
  const [show, setShow] = useState(true)
  const [arr, setArr] = useState([])
  const [theme, setTheme] = useState('light')

  function fetchDataAgian() {
    axios.get(`http://localhost:3001/mail?page=1&offset=10`)
      .then(el => el.data)
      .then(el => {
        setData(el)
      })
  }

  function fetchUpdate() {
      axios.get(`http://localhost:3001/mail?page=${pagination}&offset=10`)
        .then(el => el.data)
        .then(el => {
          const d = data
          el.forEach(item => {
            data.push(item)
          })
          setData(d)
        })
      setPagination(pagination + 1)
    }
  const getParams = () => {
    setPagination(pagination + 1)
    fetchUpdate()
  }
  const changeTheme = () => {
    if (theme === 'dark') setTheme('light')
    else setTheme('dark')
  }
  const clickStatus = (el) => {
    console.log(arr)
    let t = arr.find(i => el === i)
    const p = arr
    if (t !== undefined) {
      p.splice(t - 1, 1);
      setArr(p)
    } else {
      p.push(el)
      setArr(p)
    }
    console.log(arr)
  }

  function sendEditStatus(status) {
    axios.put('http://localhost:3001/mail', {
      keys: arr,
      status: status
      })
    }

  const drawStatus = async (status) => {
    await sendEditStatus(status)
    await fetchDataAgian()
    setTimeout(async () => {
      await fetchDataAgian()
    }, 1000)
  }
  useEffect(() => {
    function fetchData() {
      axios.get(`http://localhost:3001/mail?page=${pagination}&offset=10`)
        .then(el => el.data)
        .then(el => {
          setData(el)
        })
      setPagination(pagination + 1)
    }
    fetchData();
  }, [])
  return (
      <ConfigProvider appearance={theme}>
        <AdaptivityProvider>
        <AppRoot>
          <SplitLayout header={<PanelHeader separator={false} />}>
            <SplitCol spaced={viewWidth > ViewWidth.MOBILE}>
              <View activePanel="main">
                <Panel id="main">
                  <PanelHeader
                    before={
                      <>
                        <Button onClick={() => drawStatus(false)} style={{marginRight: "10px"}}>
                          Отметить как прочитанные
                        </Button>
                        <Button onClick={() => drawStatus(true)}>
                          Отметить не прочитанные
                        </Button>
                      </>
                    }
                  >
                    <div>
                        <PanelHeaderButton>
                          <Icon28MoonOutline onClick={changeTheme} />
                        </PanelHeaderButton>
                    </div>
                  </PanelHeader>
                  <Group>
                    {data && data.length > 0 ?
                      data.map((el, keyEl) => {
                          return <MailItem keyEl={keyEl} el={el} clickStatus={clickStatus} />
                        })
                      :
                      ''
                    }
                  </Group>
                  <Button onClick={getParams}>
                    Загрузить еще
                  </Button>
                </Panel>
              </View>
            </SplitCol>
          </SplitLayout>
         </AppRoot>
        </AdaptivityProvider>
      </ConfigProvider>
  );
}
