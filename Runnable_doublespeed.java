import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.TextField;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.image.BufferedImage;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Scanner;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;

public class Runnable_doublespeed {
	//static boolean[] flowDir = new boolean[2];
	static ArrayList<ArrayList<Integer>> inputs= new ArrayList<ArrayList<Integer>>();
	static int carCounter;
	static ArrayList<JButton> buttonsIn = new ArrayList<JButton>();
	//<vehicle id="vehicle_4" depart="0.00" departLane="best" departSpeed="speedLimit" route="route_1" />
    public static void main(String[] args) throws Exception {
    	inputs.add(new ArrayList<Integer>());
    	inputs.add(new ArrayList<Integer>());
    	inputs.add(new ArrayList<Integer>());
    	inputs.add(new ArrayList<Integer>());

    	ArrayList<int[]> log = new ArrayList<>();
    	
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int width = screenSize.width;
        int height = screenSize.height-75;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter Car Number Start: ");
        carCounter = scanner.nextInt();
        System.out.println("Enter Car Time Start: ");
        int startTime = scanner.nextInt();
        double startTimeGlobal = System.currentTimeMillis();
        
        String file = "C:/Users/Jackson/Downloads/MequonAndBuntrockIntersection.png";
        BufferedWriter output = new BufferedWriter(new FileWriter("C:/Users/Jackson/Desktop/CarData/Day14.Thursday.12.19.19.txt", true));
        
        ImageIcon myImage = new ImageIcon(file);
        myImage = resizeImageIcon(myImage,width,height);
        JFrame f = new JFrame("Data Collection");
        f.setContentPane(new ImagePanel(myImage.getImage()));
        
        for(int x = 0; x<18;x++) {
        	buttonsIn.add(new JButton());
        }
        /*
        f.addMouseListener(new MouseListener() {
            public void mousePressed(MouseEvent me) { }
            public void mouseReleased(MouseEvent me) { }
            public void mouseEntered(MouseEvent me) { }
            public void mouseExited(MouseEvent me) { }
            public void mouseClicked(MouseEvent me) { 
              int x = me.getX();
              int y = me.getY();
              System.out.println("X:" + x + " Y:" + y); 
            }
        });
        */
        for(JButton b:buttonsIn) {
        	
        	
        	
        	b.removeMouseListener(b.getMouseListeners()[0]);
        	if(buttonsIn.indexOf(b)<4) {
        		b.setBorderPainted(false);
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				
        				int buttonId = buttonsIn.indexOf(b);
        				int TimeStamp =  (int) Math.round(System.currentTimeMillis()/1000-startTimeGlobal/1000)*2+startTime;
        				System.out.println("STRAIGHT--TimeStamp: " + TimeStamp + ", buttonId: " + buttonId);
        				inputs.get(buttonId).add(TimeStamp);
        				b.setText(""+inputs.get(buttonId).size());
        			}
        		});
        	}else if(buttonsIn.indexOf(b)==4) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(2).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
								output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(2).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_7\" />");
								carCounter++;
    						} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(2).remove(0);
    						buttonsIn.get(2).setText(""+inputs.get(2).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}else if(buttonsIn.indexOf(b)==5) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(1).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(1).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_5\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(1).remove(0);
    						buttonsIn.get(1).setText(""+inputs.get(1).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}else if(buttonsIn.indexOf(b)==6) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(3).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(3).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_9\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(3).remove(0);
    						buttonsIn.get(3).setText(""+inputs.get(3).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==7) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(3).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(3).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_10\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(3).remove(0);
    						buttonsIn.get(3).setText(""+inputs.get(3).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==8) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(2).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(2).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_8\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(2).remove(0);
    						buttonsIn.get(2).setText(""+inputs.get(2).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==9) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(0).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(0).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_0\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(0).remove(0);
    						buttonsIn.get(0).setText(""+inputs.get(0).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==10) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(0).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(0).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_1\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(0).remove(0);
    						buttonsIn.get(0).setText(""+inputs.get(0).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==11) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(3).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(3).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_11\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(3).remove(0);
    						buttonsIn.get(3).setText(""+inputs.get(3).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==12) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(1).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(1).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_3\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(1).remove(0);
    						buttonsIn.get(1).setText(""+inputs.get(1).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==13) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(1).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(1).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_4\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(1).remove(0);
    						buttonsIn.get(1).setText(""+inputs.get(1).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==14) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(0).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(0).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_2\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(0).remove(0);
    						buttonsIn.get(0).setText(""+inputs.get(0).size());
    					}else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	else if(buttonsIn.indexOf(b)==15) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				if(inputs.get(2).size()!=0) {
    						try {
    							System.out.println("ADDED");
    							output.newLine();
    							output.write("<vehicle id=\"vehicle_" + carCounter + "\" depart=\"" + inputs.get(2).get(0) + "\" departLane=\"best\" departSpeed=\"speedLimit\" route=\"route_6\" />");
								carCounter++;
							} catch (IOException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
								System.out.println("NOT WRITTEN!");
							}
    						inputs.get(2).remove(0);
    						buttonsIn.get(2).setText(""+inputs.get(2).size());
    					}
        				else {
    						System.out.println("NO CARS THERE");
    					}
        			}
        		});
        	}
        	/*
        	else if(buttonsIn.indexOf(b)<10) {
        		b.addMouseListener(new java.awt.event.MouseAdapter(){
        			public void mousePressed(java.awt.event.MouseEvent evt){
        				int buttonId = buttonsIn.indexOf(b);
        				int TimeStamp =  (int) Math.round(System.currentTimeMillis()/1000-startTimeGlobal/1000+startTime);
        				System.out.println("LEFT--TimeStamp: " + TimeStamp + ", buttonId: " + buttonId);
        				leftTurnInputs.get(buttonId-8).add(TimeStamp);
        			}
        		});
        	}
        	*/
        	if(buttonsIn.indexOf(b)==0) {
        		b.setBackground(new Color(100,200,128,255));
        		b.setBounds(375,384,169, 88);
        	}
        	if(buttonsIn.indexOf(b)==1) {
        		b.setBackground(new Color(100,200,128,255));
        		b.setBounds(634,466,50, 94);
        	}
        	if(buttonsIn.indexOf(b)==2) {
        		b.setBackground(new Color(100,200,128,255));
        		b.setBounds(714,284,195, 80);
        	}
        	if(buttonsIn.indexOf(b)==3) {
        		b.setBackground(new Color(100,200,128,255));
        		b.setBounds(566,165,50, 97);
        	}
        	if(buttonsIn.indexOf(b)==4) {
        		b.setBackground(new Color(255,100,100,128));
        		b.setBounds(480,317,75,47);
        	}
        	if(buttonsIn.indexOf(b)==5) {
        		b.setBackground(new Color(200,100,100,128));
        		b.setBounds(405,317,75,47);
        	}
        	if(buttonsIn.indexOf(b)==6) {
        		b.setBackground(new Color(155,100,100,128));
        		b.setBounds(330,317,75,47);
        	}
        	if(buttonsIn.indexOf(b)==7) {
        		b.setBackground(new Color(255,100,100,128));
        		b.setBounds(593,456,39, 50);
        	}
        	if(buttonsIn.indexOf(b)==8) {
        		b.setBackground(new Color(200,100,100,128));
        		b.setBounds(593,506,39, 50);
        	}
        	if(buttonsIn.indexOf(b)==9) {
        		b.setBackground(new Color(155,100,100,128));
        		b.setBounds(593,556,39, 50);
        	}
        	if(buttonsIn.indexOf(b)==10) {
        		b.setBackground(new Color(255,100,100,128));
        		b.setBounds(725,385,60, 57);
        	}
        	if(buttonsIn.indexOf(b)==11) {
        		b.setBackground(new Color(200,100,100,128));
        		b.setBounds(785,385,60, 57);
        	}
        	if(buttonsIn.indexOf(b)==12) {
        		b.setBackground(new Color(155,100,100,128));
        		b.setBounds(845,385,60, 57);
        	}
        	if(buttonsIn.indexOf(b)==13) {
        		b.setBackground(new Color(255,100,100,128));
        		b.setBounds(620,214,33, 50);
        	}
        	if(buttonsIn.indexOf(b)==14) {
        		b.setBackground(new Color(200,100,100,128));
        		b.setBounds(620,164,33, 50);
        	}
        	if(buttonsIn.indexOf(b)==15) {
        		b.setBackground(new Color(155,100,100,128));
        		b.setBounds(620,114,33, 50);
        	}
        	
        	
        	f.add(b);
        }
        
        
        JButton flush = new JButton("Flush");
        flush.setBorderPainted(false);
        flush.setBackground(new Color(200,200,200,255));
        flush.setBounds(width-100,0,100,100);
        flush.addMouseListener(new java.awt.event.MouseAdapter(){
            public void mousePressed(java.awt.event.MouseEvent evt){
            	try {
            		System.out.println("FLUSH COMPLETE");
					output.flush();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					System.out.println("NOT FLUSHED!!!!");
				}
            }
        });
        f.add(flush);
        /*
        JButton meqGreen = new JButton("Mequon Green");
        meqGreen.setBorderPainted(false);
        meqGreen.setBackground(new Color(200,200,200,255));
        meqGreen.setBounds(width-200,0,100,100);
        meqGreen.addMouseListener(new java.awt.event.MouseAdapter(){
            public void mousePressed(java.awt.event.MouseEvent evt){
            	System.out.println("-----------MEQUON GREEN------------");
            	flowDir[0] = true;
            	flowDir[1] = false;
            }
        });
        f.add(meqGreen);
        JButton buntGreen = new JButton("Buntrock Green");
        buntGreen.setBorderPainted(false);
        buntGreen.setBackground(new Color(200,200,200,255));
        buntGreen.setBounds(width-300,0,100,100);
        buntGreen.addMouseListener(new java.awt.event.MouseAdapter(){
            public void mousePressed(java.awt.event.MouseEvent evt){
            	flowDir[1] = true;
            	System.out.println("-----------BUNKTROCK GREEN------------");
            	flowDir[0] = false;
            }
        });
        f.add(buntGreen);
        */
        f.setSize(width,height);    
		f.setLayout(null);   
		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setVisible(true);

        
        while (true) {
        	Thread.sleep(1000);
        }
        
        
    }
    public static ImageIcon resizeImageIcon( ImageIcon imageIcon , Integer width , Integer height )
    {
        BufferedImage bufferedImage = new BufferedImage( width , height , BufferedImage.TRANSLUCENT );

        Graphics2D graphics2D = bufferedImage.createGraphics();
        graphics2D.drawImage( imageIcon.getImage() , 0 , 0 , width , height , null );
        graphics2D.dispose();

        return new ImageIcon( bufferedImage , imageIcon.getDescription() );
    }
}
