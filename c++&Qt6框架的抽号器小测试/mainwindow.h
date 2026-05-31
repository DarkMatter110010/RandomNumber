#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMap>
#include <QJsonObject>
#include <QJsonDocument>
#include <QFile>
#include <QRandomGenerator>
#include <QLabel>
#include <QPushButton>
#include <QMessageBox>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QMenu>
#include <QMenuBar>
#include <QDialog>
#include <QSpinBox>
#include <QComboBox>
#include <QSlider>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget* parent = nullptr);
    ~MainWindow();

private:
    void loadJsonData();
    void saveJsonData();
    int getWeightedRandom();
    void initUI();
    void createMenu();

    QLabel* m_resultLabel;
    QPushButton* m_drawBtn;
    QPushButton* m_clearBtn;

    QMap<int, int> m_numbers;
    QString m_jsonFile = "number.json";
};

// --- 1. 修改范围的弹窗 ---
class RangeDialog : public QDialog {
    Q_OBJECT
public:
    RangeDialog(QWidget* parent = nullptr) : QDialog(parent) {
        this->setWindowTitle("修改号码范围");
        this->resize(300, 150);
        QVBoxLayout* layout = new QVBoxLayout(this);

        QHBoxLayout* startLayout = new QHBoxLayout();
        startLayout->addWidget(new QLabel("起始号码:"));
        startSpin = new QSpinBox();
        startSpin->setRange(1, 9999);
        startSpin->setValue(1);
        startLayout->addWidget(startSpin);
        layout->addLayout(startLayout);

        QHBoxLayout* endLayout = new QHBoxLayout();
        endLayout->addWidget(new QLabel("结束号码:"));
        endSpin = new QSpinBox();
        endSpin->setRange(1, 9999);
        endSpin->setValue(50);
        endLayout->addWidget(endSpin);
        layout->addLayout(endLayout);

        QPushButton* okBtn = new QPushButton("确定");
        connect(okBtn, &QPushButton::clicked, this, [this]() {
            if (startSpin->value() > endSpin->value()) {
                QMessageBox::warning(this, "错误", "起始号码不能大于结束号码！");
            }
            else {
                this->accept();
            }
            });
        layout->addWidget(okBtn);
    }
    int getStart() { return startSpin->value(); }
    int getEnd() { return endSpin->value(); }
private:
    QSpinBox* startSpin;
    QSpinBox* endSpin;
};

// --- 2. 修改权重的弹窗 ---
class WeightDialog : public QDialog {
    Q_OBJECT
public:
    WeightDialog(QMap<int, int> numbers, QWidget* parent = nullptr) : QDialog(parent), m_numbers(numbers) {
        this->setWindowTitle("修改单个号码权重");
        this->resize(350, 200);

        QVBoxLayout* mainLayout = new QVBoxLayout(this);

        // --- 第一行：下拉框选号码 ---
        QHBoxLayout* numLayout = new QHBoxLayout();
        numLayout->addWidget(new QLabel("选择号码:"));
        m_comboNumber = new QComboBox();
        for (auto it = m_numbers.begin(); it != m_numbers.end(); ++it) {
            m_comboNumber->addItem(QString::number(it.key()), it.key());
        }
        numLayout->addWidget(m_comboNumber);
        mainLayout->addLayout(numLayout);

        // --- 第二行：滑动条和数值显示 ---
        QHBoxLayout* sliderLayout = new QHBoxLayout();
        sliderLayout->addWidget(new QLabel("权重 (0-50):"));

        m_sliderWeight = new QSlider(Qt::Horizontal);
        m_sliderWeight->setRange(0, 50);
        m_sliderWeight->setValue(1);
        sliderLayout->addWidget(m_sliderWeight);

        m_labelWeightVal = new QLabel("1");
        m_labelWeightVal->setFixedWidth(30);
        m_labelWeightVal->setAlignment(Qt::AlignCenter);
        sliderLayout->addWidget(m_labelWeightVal);

        mainLayout->addLayout(sliderLayout);

        connect(m_sliderWeight, &QSlider::valueChanged, this, [this](int val) {
            m_labelWeightVal->setText(QString::number(val));
            });

        // --- 第三行：三个按钮 ---
        QHBoxLayout* btnLayout = new QHBoxLayout();

        m_btnApply = new QPushButton("应用");
        m_btnApply->setToolTip("立即保存修改，不关闭窗口");
        btnLayout->addWidget(m_btnApply);

        m_btnOK = new QPushButton("确定");
        m_btnOK->setToolTip("保存修改并关闭窗口");
        btnLayout->addWidget(m_btnOK);

        m_btnCancel = new QPushButton("取消");
        m_btnCancel->setToolTip("放弃修改并关闭");
        btnLayout->addWidget(m_btnCancel);

        mainLayout->addLayout(btnLayout);
    }

    void initCurrentWeight() {
        int currentNum = m_comboNumber->currentData().toInt();
        if (m_numbers.contains(currentNum)) {
            m_sliderWeight->setValue(m_numbers[currentNum]);
        }
    }

    int getSelectedNumber() { return m_comboNumber->currentData().toInt(); }
    int getSelectedWeight() { return m_sliderWeight->value(); }

public:
    QPushButton* m_btnApply;
    QPushButton* m_btnOK;
    QPushButton* m_btnCancel;

private:
    QMap<int, int> m_numbers;
    QComboBox* m_comboNumber;
    QSlider* m_sliderWeight;
    QLabel* m_labelWeightVal;
};

#endif // MAINWINDOW_H